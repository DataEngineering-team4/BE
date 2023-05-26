import json

from django.core.files import File
from django.test import Client, TestCase

from drawing.models import Animation, Drawing
from user.models import User


# Create your tests here.
class DrawingViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="t_username", email="t_email@test.test", password="t_password")
        self.client = Client()
        self.drawing = Drawing.objects.create(
            user=self.user, name="t_drawing")
        self.drawing.file.name = "core/tests/src/test_drawing.png"
        self.drawing.save()
        self.animation = Animation.objects.create(
            drawing=self.drawing, purpose="wait1")
        self.animation.file.name = "core/tests/src/test_drawing.png"
        self.animation.save()
        self.wrong_user_id = 10000
        self.wrong_drawing_id = 10000

    def drawing_get_test(self, user_id, drawing_list, message, status_code):
        response = self.client.get(f'/drawing/?user_id={user_id}')
        data = json.loads(response.content)
        if drawing_list:
            self.assertEqual(data, drawing_list)
        self.assertEqual(response.status_code, status_code)
        if message:
            self.assertEqual(data["message"], message)

    def test_drawing_get(self):
        drawing_list = [{
            "id": self.drawing.id,
            "name": self.drawing.name,
            "link": f"{self.drawing.file.url}",
            "status": self.drawing.status
        }]
        self.drawing_get_test(self.user.id, drawing_list, "", 200)
        self.drawing_get_test(self.wrong_user_id, None,
                              "User does not exist", 400)

    def drawing_post_test(self, drawing_dict, message, status_code):
        response = self.client.post(f'/drawing/', data=drawing_dict)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status_code)
        if message:
            self.assertEqual(data["message"], message)

    def test_drawing_post(self):
        data = {
            "user_id": self.user.id,
            "name": "new_test_drwaing",
            "file": open("core/tests/src/test_photo.png", "rb")
        }
        self.drawing_post_test(data, "Image Uploaded Successfully", 200)
        data = {
            "user_id": self.wrong_user_id,
            "name": "new_test_drwaing",
            "file": open("core/tests/src/test_photo.png", "rb")
        }
        self.drawing_post_test(data, "User does not exist", 400)

    def animation_get_test(self, user_id, drawing_id, animation_list, message, status_code):
        response = self.client.get(
            f'/animation/?user_id={user_id}&drawing_id={drawing_id}')
        data = json.loads(response.content)
        if animation_list:
            self.assertEqual(data, animation_list)
        self.assertEqual(response.status_code, status_code)
        if message:
            self.assertEqual(data["message"], message)

    def test_animation_get(self):
        animation_list = [{
            "id": self.animation.id,
            "drawing_id": self.animation.drawing.id,
            "purpose": self.animation.purpose,
            "link": f"{self.animation.file.url}",
        }]
        self.animation_get_test(
            self.user.id, self.drawing.id, animation_list, "", 200)
        self.animation_get_test(self.wrong_user_id, self.drawing.id, None,
                                "User does not exist", 400)
        self.animation_get_test(self.user.id, self.wrong_drawing_id, None,
                                None, 400)

    def animation_post_test(self, animation_dict, message, status_code):
        response = self.client.post(f'/animation/', data=animation_dict)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status_code)
        if message:
            self.assertEqual(data["message"], message)

    def test_animation_post(self):
        data = {
            "drawing_id": self.drawing.id,
            "purpose": "wait1",
            "file": open("core/tests/src/test_photo.png", "rb")
        }
        self.animation_post_test(data, "Image Uploaded Successfully", 200)
        data = {
            "drawing_id": self.wrong_drawing_id,
            "purpose": "wait2",
            "file": open("core/tests/src/test_photo.png", "rb")
        }
        self.animation_post_test(data, "Drawing does not exist", 400)
