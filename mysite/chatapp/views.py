from django.views.generic import ListView, DetailView
from django.shortcuts import render

from .models import ChatRoom
from .services import ChatService


class RoomListView(ListView):
    """List all chat rooms."""
    model = ChatRoom
    template_name = 'chatapp/index.html'
    context_object_name = 'chatrooms'


class RoomDetailView(DetailView):
    """Show a single room and recent messages."""
    model = ChatRoom
    template_name = 'chatapp/room.html'
    context_object_name = 'chatroom'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.object
        context['messages'] = ChatService.get_recent_messages(room, limit=30)
        return context