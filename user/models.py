from asgiref.sync import sync_to_async
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for MJ23.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    @classmethod
    async def get_user(cls, username):
        users = await sync_to_async(list)(User.objects.filter(username=username))
        return users[0] if len(users) > 0 else None

    async def get_room_name(self):
        room_count = await self.get_room_count()
        return self.username + str(room_count)

    async def get_room_count(self):
        return len(await sync_to_async(list)(self.rooms.all()))

    def __str__(self):
        return self.username
