from django.db import models

from core.models import TimeStampedModel
from user.models import User

MESSAGE_ROLE_CHOICES = (
    ("system", "초기설정"), ("assistant", "GPT"), ("user", "유저"),
)


class Room(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rooms")
    count = models.IntegerField()

    def __str__(self):
        return f"{self.user.username}의 {self.count}번째 방"


class Message(TimeStampedModel):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="messages")
    audio_url = models.URLField()
    text = models.TextField()
    role = models.CharField(max_length=10, choices=MESSAGE_ROLE_CHOICES)

    def __str__(self):
        return f"[{str(self.room)}] {self.role}: {self.text}"
