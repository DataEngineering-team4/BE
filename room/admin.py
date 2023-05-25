from django.contrib import admin
from django.utils.safestring import mark_safe

from room.models import Message, Room

# Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "count",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "room",
        "count",
        "detail_url",
        "text",
        "role",
    )

    def detail_url(self, instance):
        url = instance.audio_url
        return mark_safe(f'<a href="{url}" target="_blank" rel="nofollow"">Sound Link</a>')
