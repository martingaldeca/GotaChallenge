from django.test import TestCase

from core.api.serializers import ActionSerializer
from core.models import Action


class ActionSerializerTest(TestCase):

    def setUp(self) -> None:
        self.action_name = 'test_name'
        self.action_description = 'test_description'

    def test_data(self):
        data = {
            'name': self.action_name,
            'description': self.action_description,
        }
        serializer = ActionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.assertEqual(Action.objects.count(), 0)
        serializer.save()
        self.assertEqual(Action.objects.count(), 1)
        action = Action.objects.last()
        self.assertEqual(action.name, self.action_name)
        self.assertEqual(action.description, self.action_description)

        expected = {
            'uuid': action.uuid.hex,
            'name': action.name,
            'description': action.description,
        }
        self.assertEqual(serializer.data, expected)
