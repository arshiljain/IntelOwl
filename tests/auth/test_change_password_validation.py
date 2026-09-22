from django.test import tag
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from . import CustomOAuthTestCase

change_password_uri = reverse("auth_changepassword")

@tag("api", "user")
class TestChangePasswordValidation(CustomOAuthTestCase):
    def setUp(self):
        self.user.set_password("hunter2")
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_missing_old_password(self):
        response = self.client.post(
            change_password_uri,
            {"new_password": "veryStrongPassword123"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Old password is required")

    def test_empty_old_password(self):
        response = self.client.post(
            change_password_uri,
            {"old_password": "", "new_password": "veryStrongPassword123"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Old password is required")
