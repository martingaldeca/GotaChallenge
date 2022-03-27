from unittest import mock

from django.test import TestCase

from core.api.serializers import ActionSerializer
from core.factories import UserFactory
from core.models import Action, User


class ActionSerializerTest(TestCase):

    def setUp(self) -> None:
        self.user: User = UserFactory()
        self.request = mock.MagicMock
        self.request.user = self.user
        self.context = {
            'request': self.request
        }
        self.action_name = 'test_name'
        self.action_description = 'test_description'

    def test_data(self):
        data = {
            'name': self.action_name,
            'description': self.action_description,
        }
        serializer = ActionSerializer(data=data, context=self.context)
        serializer.is_valid()
        self.assertEqual(Action.objects.count(), 0)
        serializer.save()
        self.assertEqual(Action.objects.count(), 1)
        action = Action.objects.last()
        self.assertEqual(action.name, self.action_name)
        self.assertEqual(action.description, self.action_description)
