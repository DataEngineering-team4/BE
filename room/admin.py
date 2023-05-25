from django.contrib import admin

from room.models import Message, Room

# Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "pk",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "room",
        "audio_url",
        "text",
        "role",
    )
