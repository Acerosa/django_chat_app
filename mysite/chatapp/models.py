from django.db import models
from django.contrib.auth.models import User

# Data model for rooms and messages. Keep the model lean; business logic lives
# in the ChatService (services.py).
class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return f"{self.name} ({self.slug})"
    
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message_content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering=('date',)

    def __str__(self):
        return f"{self.user.username}: {self.message_content[:30]}"

    @classmethod
    def recent_for_room(cls, room: ChatRoom, limit: int = 30):
        return cls.objects.filter(room=room).order_by('-date')[:limit]
