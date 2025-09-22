from typing import List

from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import ChatRoom, ChatMessage


class ChatService:
    """Domain service for chat operations.

    Encapsulates business logic for fetching rooms/messages and persisting new
    messages from authenticated users. Keeping this logic here improves
    separation of concerns between transport layers (HTTP/WebSocket) and data.
    """

    @staticmethod
    def get_room_by_slug(slug: str) -> ChatRoom:
        """Return a room by slug or 404 if not found."""
        return get_object_or_404(ChatRoom, slug=slug)

    @staticmethod
    def get_recent_messages(room: ChatRoom, limit: int = 30) -> List[ChatMessage]:
        """Return most recent messages in chronological order (oldest → newest)."""
        recent_qs = ChatMessage.recent_for_room(room, limit=limit)
        # recent_for_room returns newest-first; reverse to chronological
        return list(recent_qs)[::-1]

    @staticmethod
    def save_message_from_user(user: User, room: ChatRoom, message_text: str) -> ChatMessage:
        """Persist a new message from a user into a room after validation."""
        cleaned = (message_text or "").strip()
        if not cleaned:
            raise ValueError("Message cannot be empty")
        with transaction.atomic():
            return ChatMessage.objects.create(
                user=user,
                room=room,
                message_content=cleaned,
            )


