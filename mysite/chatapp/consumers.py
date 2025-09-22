from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser
from .services import ChatService


class ChatConsumer(AsyncWebsocketConsumer):
    """Channels consumer handling real-time chat over WebSockets.

    Responsibilities:
    - Manage group membership for a given room
    - Accept messages from an authenticated user, persist, and broadcast
    - Emit events to clients in the same room
    """

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Handle an incoming message from the client.

        Expects JSON with keys: message, room. Uses the authenticated user
        from the scope; rejects unauthenticated clients.
        """
        data = json.loads(text_data)
        message = data.get('message', '')
        room_slug = data.get('room')

        user = self.scope.get('user')
        if not user or isinstance(user, AnonymousUser) or not user.is_authenticated:
            await self.send(text_data=json.dumps({'error': 'auth_required'}))
            return

        try:
            room = await self.get_room(room_slug)
            await self.save_message(user, room, message)
        except Exception as exc:
            await self.send(text_data=json.dumps({'error': 'invalid_request'}))
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': user.username,
                'room': room_slug,
            }
        )
        
    async def chat_message(self,event):
        """Forward a broadcast message to the connected client."""
        message = event['message']
        username = event['username']
        room = event['room']
        
        await self.send(text_data=json.dumps({
            'message':message,
            'username':username,
            'room':room,
        }))
    
    @sync_to_async
    def save_message(self, user, room, message):
        ChatService.save_message_from_user(user=user, room=room, message_text=message)

    @sync_to_async
    def get_room(self, slug):
        return ChatService.get_room_by_slug(slug)
    