from core.api.serializers import MeSerializer
from core.api.views.tests.base import APITestBase
from core.models import User
from django.urls import reverse
from rest_framework import status


class RegisterViewTest(APITestBase):
    url = reverse('core:register')

    def test_post_201_CREATED(self):
        username = 'test'
        email = 'test@test.test'
        password = 'testpass'
        data_to_send = {
            'username': username,
            'email': email,
            'password': password,
        }
        self.assertEqual(User.objects.count(), 1)
        response = self.client.post(self.url, data=data_to_send)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data)
        self.assertEqual(User.objects.count(), 2)
        user = User.objects.last()
        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


class MeDetailViewTest(APITestBase):
    url = reverse('core:me')

    def test_get_200_OK(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, MeSerializer(instance=self.user, context=self.test_context).data)
