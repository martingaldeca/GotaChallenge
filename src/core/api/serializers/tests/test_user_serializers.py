from django.test import TestCase

from core.api.serializers import SimpleUserSerializer, MeSerializer
from core.factories import UserFactory
from core.models import User


class SimpleUserSerializerTest(TestCase):

    def test_data(self):
        user: User = UserFactory()
        expected_data = {
            'uuid': user.uuid.hex,
            'username': user.username,
        }
        self.assertEqual(SimpleUserSerializer(instance=user).data, expected_data)


class MeSerializerTest(TestCase):
    def test_data(self):
        user: User = UserFactory()
        expected_data = {
            'uuid': user.uuid.hex,
            'username': user.username,
            'email': user.email,
        }
        self.assertEqual(MeSerializer(instance=user).data, expected_data)
