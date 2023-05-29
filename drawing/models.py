from django.db import models

from core.models import TimeStampedModel
from user.models import User

DRAWING_STATUS_CHOICES = (
    ("pending", "승인필요"), ("approved", "승인됨"), ("active", "활성"), ("inactive", "비활성"),
)

ANIMATIOIN_PURPOSE_CHOICES = (
    ("wait1", "대기1"), ("wait2", "대기2"), ("listen1", "듣는중1"),
    ("listen2", "듣는중2"), ("talking1", "말하는중1"), ("talking2", "말하는중2")
)


class Drawing(TimeStampedModel):
    class Meta:
        ordering = ['-created_at']
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="drawings")
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="drawing")
    status = models.CharField(
        max_length=15, choices=DRAWING_STATUS_CHOICES, default="active")

    def __str__(self):
        return f"{self.user.username}의 {self.name}"


class Animation(TimeStampedModel):
    class Meta:
        ordering = ['-created_at']
    drawing = models.ForeignKey(
        Drawing, on_delete=models.CASCADE, related_name="animations")
    file = models.FileField(upload_to="animation")
    purpose = models.CharField(
        max_length=10, choices=ANIMATIOIN_PURPOSE_CHOICES)

    def __str__(self):
        return f"[{str(self.drawing)}] {self.purpose}"
