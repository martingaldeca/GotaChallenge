from core.factories import UserFactory
from core.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory


class APITestBase(APITestCase):
    url = None

    def setUp(self) -> None:
        self.user: User = UserFactory(password='root1234')
        self.client.login(username=self.user.username, password='root1234')
        response = self.client.post(
            reverse('login'),
            {
                'username': self.user.username,
                'password': 'root1234'
            }
        )
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        self.test_context = {'request': APIRequestFactory().get(self.url)}

    def assertSameFile(self, file1, file2):
        file1.seek(0)
        file2.seek(0)
        self.assertEqual(file1.read(), file2.read())
