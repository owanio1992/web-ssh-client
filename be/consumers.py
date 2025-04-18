import json

from channels.generic.websocket import WebsocketConsumer

class SSHConsumer(WebsocketConsumer):
    def connect(self):
        self.server_id = self.scope['url_route']['kwargs']['server_id']
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))