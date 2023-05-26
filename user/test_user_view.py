import json

from django.test import Client, TestCase

from user.models import User


# Create your tests here.
class UserViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="t_username", email="t_email@test.test", password="t_password")
        self.client = Client()

    def user_signup_test(self, user_signp_dict, message, status_code):
        response = self.client.post('/user/signup/',
                                    json.dumps(user_signp_dict),
                                    content_type="application/json")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status_code)
        if message:
            self.assertEqual(data["message"], message)

    def test_user_signup(self):
        new_user_signp_dict = {
            "username": "t_username2",
            "password": "t_password2",
            "email": "t_email2@test.test"
        }
        self.user_signup_test(new_user_signp_dict,
                              "User registered successfully", 200)
        already_exist_user_signp_dict = {
            "username": "t_username",
            "password": "t_password2",
            "email": "t_email2@test.test"
        }
        self.user_signup_test(already_exist_user_signp_dict,
                              "Username Already Exists", 400)
        errored_user_signp_dict = {
            "password": "password",
            "email": "t_email3@test.test"
        }
        self.user_signup_test(errored_user_signp_dict,
                              "", 500)

    def uset_login_test(self, user_login_dict, message, status_code):
        response = self.client.post('/user/login/',
                                    json.dumps(user_login_dict),
                                    content_type="application/json")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status_code)
        if message:
            self.assertEqual(data["message"], message)

    def test_user_login(self):
        user_login_dict = {
            "username": "t_username",
            "password": "t_password"
        }
        self.uset_login_test(
            user_login_dict, "User logged in successfully", 200)
        wrong_password_user_login_dict = {
            "username": "t_username",
            "password": "wrong_password"
        }
        self.uset_login_test(
            wrong_password_user_login_dict, "비밀번호가 틀렸습니다.", 400
        )
        not_exist_user_login_dict = {
            "username": "wrong_username",
            "password": "t_password"
        }
        self.uset_login_test(not_exist_user_login_dict, "존재하지 않는 아이디입니다.", 400)
        error_user_login_dict = {
            "password": "t_password"
        }
        self.uset_login_test(error_user_login_dict,
                             "", 500)
