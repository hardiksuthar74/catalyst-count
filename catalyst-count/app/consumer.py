import json
from channels.generic.websocket import WebsocketConsumer


class TaskProgressConsumer(WebsocketConsumer):
    def connect(self):
        self.task_id = self.scope["url_route"]["kwargs"]["task_id"]
        self.group_name = f"task_progress_{self.task_id}"

        # Add this WebSocket connection to the task-specific group
        self.channel_layer.group_add(self.group_name, self.channel_name)

        self.accept()

    def disconnect(self, close_code):
        # Remove this WebSocket connection from the task-specific group
        self.channel_layer.group_discard(self.group_name, self.channel_name)

    def send_progress(self, event):
        # Send progress data to the WebSocket
        self.send(text_data=json.dumps(event["progress_data"]))
