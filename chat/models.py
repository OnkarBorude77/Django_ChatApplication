from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    """
    Direct message room created from two usernames in sorted order.
    e.g. 'alice__bob'
    """
    name = models.CharField(max_length=255, unique=True)
    participants = models.ManyToManyField(User, related_name="chat_rooms", blank=True)

    def __str__(self):
        return self.name

    @staticmethod
    def dm_room_name(u1: str, u2: str) -> str:
        return "__".join(sorted([u1.lower(), u2.lower()]))

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"
