from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from drawing.models import Animation, Drawing

# Register your models here.


@admin.register(Drawing)
class DrawingAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "name",
        "status",
    )


@admin.register(Animation)
class AnimationAdmin(admin.ModelAdmin):
    list_display = (
        "drawing",
        "detail_url",
        "purpose",
    )

    def detail_url(self, instance):
        url = instance.file.url
        return mark_safe(f'<a href="{url}" target="_blank" rel="nofollow"">Animation Link</a>')
