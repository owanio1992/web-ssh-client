import json
import paramiko
import threading
import io
import traceback
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)
from django.shortcuts import get_object_or_404
from .models import Server
from asgiref.sync import sync_to_async
class SSHConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info("SSHConsumer: Entering connect method.")
        self.server_id = self.scope['url_route']['kwargs']['server_id']
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.ssh_client = None
        self.channel = None
        self.read_thread = None

        logger.info(f"SSHConsumer: Attempting to accept WebSocket connection for server_id={self.server_id}, session_id={self.session_id}")
        await self.accept()
        logger.info(f"SSHConsumer: WebSocket connection accepted for server_id={self.server_id}, session_id={self.session_id}")


        import datetime
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"SSHConsumer: WebSocket connection established at {current_time}. Sending current time to frontend.")
        await self.send(text_data=json.dumps({
            'type': 'time_update',
            'time': current_time
        }))

        try:
            logger.info(f"SSHConsumer: WebSocket connected for server_id={self.server_id}, session_id={self.session_id}")
            # Fetch server and SSH key details
            logger.info("SSHConsumer: Fetching server details...")
            server = await self.get_server(self.server_id)
            logger.info(f"SSHConsumer: Fetched server details for {server.site_name} - {server.server_name}")
            ssh_key = await sync_to_async(lambda: server.ssh_key)()
            # Decrypt the SSH key
            logger.info("SSHConsumer: Decrypting SSH key...")
            ssh_key_content = ssh_key.decrypt_key()
            logger.info("SSHConsumer: SSH key decrypted.")

            # Establish SSH connection
            logger.info("SSHConsumer: Initializing SSH client...")
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            logger.info("SSHConsumer: SSH client initialized.")

            # Load the private key
            logger.info("SSHConsumer: Loading private key...")
            # Use sync_to_async for synchronous key loading
            pkey = await sync_to_async(paramiko.RSAKey.from_private_key)(io.StringIO(ssh_key_content))
            logger.info("SSHConsumer: Private key loaded.")

            logger.info(f"SSHConsumer: Attempting to connect to {server.host} as {server.user}...")
            # Use sync_to_async for synchronous SSH connection
            await sync_to_async(self.ssh_client.connect)(server.host, username=server.user, pkey=pkey)
            logger.info("SSHConsumer: SSH connection established.")

            # Start a shell
            logger.info("SSHConsumer: Invoking shell...")
            self.channel = self.ssh_client.invoke_shell()
            logger.info("SSHConsumer: Shell invoked.")

            # Start a thread to read from the SSH channel
            self.read_thread = threading.Thread(target=self.read_from_channel, daemon=True)
            self.read_thread.start()

        except Exception as e:
            logger.error(f"SSH connection error: {e}", exc_info=True)
            await self.send(text_data=json.dumps({
                'error': f'Failed to connect to server: {e}'
            }))
            await self.close()

    async def disconnect(self, close_code):
        logger.info(f"SSHConsumer: Disconnecting with code {close_code}")
        if self.channel:
            self.channel.close()
            logger.info("SSHConsumer: SSH channel closed.")
        if self.ssh_client:
            self.ssh_client.close()
            logger.info("SSHConsumer: SSH client closed.")
        if self.read_thread and self.read_thread.is_alive():
            # It's generally not safe to forcefully stop a thread,
            # but for a daemon thread reading from a closed channel,
            # it should exit naturally. We can add a small timeout
            # if needed, but for now, rely on the channel closing.
            pass
        logger.info("SSHConsumer: Disconnect method finished.")


    async def receive(self, text_data):
        logger.info(f"SSHConsumer: Received message: {text_data}")
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message')

            if self.channel and message:
                logger.info(f"SSHConsumer: Sending message to SSH channel: {message}")
                self.channel.send(message)
        except Exception as e:
            logger.error(f"Error receiving message: {e}", exc_info=True)

    def read_from_channel(self):
        logger.info("SSHConsumer: Read thread started.")
        try:
            while not self.channel.closed:
                if self.channel.recv_ready():
                    data = self.channel.recv(1024).decode()
                    logger.info(f"SSHConsumer: Received data from channel: {data}")
                    # Send data back to the WebSocket consumer's receive method
                    from asgiref.sync import async_to_sync
                    async_to_sync(self.channel_layer.send)(
                        self.channel_name,
                        {
                            'type': 'ssh_output',
                            'output': data
                        }
                    )
                elif self.channel.recv_stderr_ready():
                    data = self.channel.recv_stderr(1024).decode()
                    logger.info(f"SSHConsumer: Received stderr from channel: {data}")
                    # Send data back to the WebSocket consumer's receive method
                    from asgiref.sync import async_to_sync
                    async_to_sync(self.channel_layer.send)(
                        self.channel_name,
                        {
                            'type': 'ssh_output',
                            'output': data
                        }
                    )
                else:
                    # Small sleep to prevent busy-waiting
                    import time
                    time.sleep(0.01)
        except Exception as e:
            logger.error(f"Error reading from channel: {e}", exc_info=True)
        finally:
            logger.info("SSHConsumer: Read thread finished.")
            # Signal the consumer to close the WebSocket
            from asgiref.sync import async_to_sync
            async_to_sync(self.channel_layer.send)(
                self.channel_name,
                {
                    'type': 'ssh_close'
                }
            )

    async def get_server(self, server_id):
        # Since Django ORM is synchronous, run it in a separate thread pool
        # or use Django's async support if available (Django 3.1+)
        # Assuming Django 3.1+ or using sync_to_async
        from asgiref.sync import sync_to_async
        return await sync_to_async(get_object_or_404)(Server, pk=server_id)

    # Handler for messages received from the read_from_channel thread
    async def ssh_output(self, event):
        logger.info(f"SSHConsumer: Sending SSH output to WebSocket: {event['output']}")
        # Send the SSH output to the WebSocket
        await self.send(text_data=json.dumps({'output': event['output']}))

    # Handler to close the WebSocket when the SSH channel closes
    async def ssh_close(self, event):
        logger.info("SSHConsumer: Received ssh_close event. Closing WebSocket.")
        await self.close()
