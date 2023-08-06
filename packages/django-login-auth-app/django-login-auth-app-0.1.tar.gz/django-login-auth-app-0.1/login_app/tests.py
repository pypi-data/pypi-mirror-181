from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class TestModelUpdates(TestCase):

    def test_user_create_and_return_username (self):
        """
        return true if user object was created and username was queried
        """
        user = User.objects.create(username="test_username", password="test_password")
        user.save()
        user.refresh_from_db()
        return self.assertEqual(user.username, "test_username")

class TestLoginViews(TestCase):

    def test_login_view_get_returns_status_code_200(self):
        """
        Return True if login_view returns a 200 http resonse
        """
        response = self.client.get(reverse("login_app:login"))
        return self.assertEqual(response.status_code, 200)

    def test_login_view_post_get_returns_status_code_200(self):
        """
        Return True if login_view returns a 200 http resonse
        """
        response = self.client.get(reverse("login_app:login_auth"))
        return self.assertEqual(response.status_code, 200)

    def test_signup_view_post_get_returns_status_code_200(self):
        """
        Return True if login_view returns a 200 http resonse
        """
        response = self.client.get(reverse("login_app:signup_auth"))
        return self.assertEqual(response.status_code, 200)
        
    def test_logout_view_returns_status_code_200(self):
        """
        Return True if login_view returns a 200 http resonse
        """
        response = self.client.get(reverse("login_app:logout"))
        return self.assertEqual(response.status_code, 200)

class TestForms(TestCase):

    def test_get_signup_and_login_form(self):
        response = self.client.get(reverse("login_app:login"))
        return self.assertIn('<input type="text"', response.content)
        
        


