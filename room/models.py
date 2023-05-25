from asgiref.sync import sync_to_async
from django.db import models

from core.models import TimeStampedModel
from user.models import User

MESSAGE_ROLE_CHOICES = (
    ("system", "초기설정"), ("assistant", "GPT"), ("user", "유저"),
)


class Room(TimeStampedModel):
    class Meta:
        ordering = ['-created_at']
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rooms")
    count = models.IntegerField(null=True, blank=True)

    async def get_messages(self):
        messages = []
        async for message in self.messages.all():
            messages.append({"role": message.role, "content": message.text})
        return messages

    def save(self, *args, **kwargs):
        if not self.count and not kwargs.get("count", None):
            self.count = self.user.rooms.all().count() + 1
        super().save(*args, **kwargs)

    async def async_save(self, *args, **kwags):
        await sync_to_async(self.save)(*args, **kwags)

    def __str__(self):
        return f"{self.user.username}의 {self.count}번째 방"


class Message(TimeStampedModel):
    class Meta:
        ordering = ['-created_at']
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="messages")
    count = models.IntegerField()
    audio_url = models.URLField()
    text = models.TextField()
    role = models.CharField(max_length=10, choices=MESSAGE_ROLE_CHOICES)

    def __str__(self):
        return f"[{str(self.room)}] {self.role}: {self.text}"

    def save(self, *args, **kwargs):
        if not self.count and not kwargs.get("count", None):
            self.count = self.room.messages.all().count() + 1
        super().save(*args, **kwargs)
