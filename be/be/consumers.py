import json
import paramiko
import asyncio
import threading
import io
import traceback
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from .models import Server, SSHKey
from asgiref.sync import sync_to_async
class SSHConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("SSHConsumer: Entering connect method.")
        self.server_id = self.scope['url_route']['kwargs']['server_id']
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.ssh_client = None
        self.channel = None
        self.read_thread = None

        print(f"SSHConsumer: Attempting to accept WebSocket connection for server_id={self.server_id}, session_id={self.session_id}") # Added log
        await self.accept()
        print(f"SSHConsumer: WebSocket connection accepted for server_id={self.server_id}, session_id={self.session_id}") # Added log


        import datetime
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"SSHConsumer: WebSocket connection established at {current_time}. Sending current time to frontend.")
        await self.send(text_data=json.dumps({
            'type': 'time_update',
            'time': current_time
        }))

        try:
            print(f"SSHConsumer: WebSocket connected for server_id={self.server_id}, session_id={self.session_id}")
            # Fetch server and SSH key details
            print("SSHConsumer: Fetching server details...")
            server = await self.get_server(self.server_id)
            print(f"SSHConsumer: Fetched server details for {server.site_name} - {server.server_name}")
            ssh_key = await sync_to_async(lambda: server.ssh_key)()
            # Decrypt the SSH key
            print("SSHConsumer: Decrypting SSH key...")
            ssh_key_content = ssh_key.decrypt_key()
            print("SSHConsumer: SSH key decrypted.")

            # Establish SSH connection
            print("SSHConsumer: Initializing SSH client...")
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print("SSHConsumer: SSH client initialized.")

            # Load the private key
            print("SSHConsumer: Loading private key...")
            # Use sync_to_async for synchronous key loading
            pkey = await sync_to_async(paramiko.RSAKey.from_private_key)(io.StringIO(ssh_key_content))
            print("SSHConsumer: Private key loaded.")

            print(f"SSHConsumer: Attempting to connect to {server.host} as {server.user}...")
            # Use sync_to_async for synchronous SSH connection
            await sync_to_async(self.ssh_client.connect)(server.host, username=server.user, pkey=pkey)
            print("SSHConsumer: SSH connection established.")

            # Start a shell
            print("SSHConsumer: Invoking shell...")
            self.channel = self.ssh_client.invoke_shell()
            print("SSHConsumer: Shell invoked.")

            # Start a thread to read from the SSH channel
            self.read_thread = threading.Thread(target=self.read_from_channel, daemon=True)
            self.read_thread.start()

        except Exception as e:
            print(f"SSH connection error: {e}")
            traceback.print_exc()
            await self.send(text_data=json.dumps({
                'error': f'Failed to connect to server: {e}'
            }))
            await self.close()

    async def disconnect(self, close_code):
        print(f"SSHConsumer: Disconnecting with code {close_code}") # Added log
        if self.channel:
            self.channel.close()
            print("SSHConsumer: SSH channel closed.") # Added log
        if self.ssh_client:
            self.ssh_client.close()
            print("SSHConsumer: SSH client closed.") # Added log
        if self.read_thread and self.read_thread.is_alive():
            # It's generally not safe to forcefully stop a thread,
            # but for a daemon thread reading from a closed channel,
            # it should exit naturally. We can add a small timeout
            # if needed, but for now, rely on the channel closing.
            pass
        print("SSHConsumer: Disconnect method finished.") # Added log


    async def receive(self, text_data):
        print(f"SSHConsumer: Received message: {text_data}") # Added log
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message')

            if self.channel and message:
                print(f"SSHConsumer: Sending message to SSH channel: {message}") # Added log
                self.channel.send(message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            traceback.print_exc()

    def read_from_channel(self):
        print("SSHConsumer: Read thread started.") # Added log
        try:
            while not self.channel.closed:
                if self.channel.recv_ready():
                    data = self.channel.recv(1024).decode()
                    print(f"SSHConsumer: Received data from channel: {data}") # Added log
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
                    print(f"SSHConsumer: Received stderr from channel: {data}") # Added log
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
            print(f"Error reading from channel: {e}")
            traceback.print_exc()
        finally:
            print("SSHConsumer: Read thread finished.") # Added log
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
        print(f"SSHConsumer: Sending SSH output to WebSocket: {event['output']}") # Added log
        # Send the SSH output to the WebSocket
        await self.send(text_data=json.dumps({'output': event['output']}))

    # Handler to close the WebSocket when the SSH channel closes
    async def ssh_close(self, event):
        print("SSHConsumer: Received ssh_close event. Closing WebSocket.") # Added log
        await self.close()