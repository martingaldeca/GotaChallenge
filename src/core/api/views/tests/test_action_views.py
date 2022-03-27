import random

from core.api.views.tests.base import APITestBase
from django.urls import reverse
from rest_framework import status

from core.api.serializers import ActionSerializer
from core.factories import ActionFactory
from core.models import Action


class ActionListViewTest(APITestBase):
    url = reverse('core:list-actions')

    def test_get_200_OK(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])
        actions = []
        for i in range(random.randint(1, 5)):
            actions.append(ActionSerializer(instance=ActionFactory()).data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], actions)


class CreateNewActionViewTest(APITestBase):
    url = reverse('core:create-action')

    def test_create_new_action_201_CREATED(self):
        action_name = 'test_name'
        action_description = 'test_description'
        data_to_send = {
            'name': action_name,
            'description': action_description,
        }
        self.assertEqual(Action.objects.count(), 0)
        response = self.client.post(self.url, data=data_to_send)
        self.assertEqual(Action.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        action = Action.objects.last()
        self.assertEqual(response.data, ActionSerializer(instance=action).data)
        self.assertEqual(action.name, action_name)
        self.assertEqual(action.description, action_description)

    def test_create_new_action_repeated_name_400_BAD_REQUEST(self):
        action_name = 'test_name'
        action_description = 'test_description'
        data_to_send = {
            'name': action_name,
            'description': action_description,
        }
        self.assertEqual(Action.objects.count(), 0)
        response = self.client.post(self.url, data=data_to_send)
        self.assertEqual(Action.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        action = Action.objects.last()
        self.assertEqual(response.data, ActionSerializer(instance=action).data)
        self.assertEqual(action.name, action_name)
        self.assertEqual(action.description, action_description)

        response = self.client.post(self.url, data=data_to_send)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(list(response.data.keys()), ['name', ])


class RetrieveUpdateDestroyActionViewTest(APITestBase):
    url = reverse('core:action', kwargs={'uuid': None})

    def test_get_action_200_OK(self):
        action: Action = ActionFactory()
        self.url = reverse('core:action', kwargs={'uuid': action.uuid.hex})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ActionSerializer(instance=action).data)

    def test_update_action_200_OK(self):
        action: Action = ActionFactory()
        self.url = reverse('core:action', kwargs={'uuid': action.uuid.hex})

        new_name = 'test_name_2'
        new_description = 'test_description_2'
        data = {
            'name': new_name,
            'description': new_description,
        }

        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        action.refresh_from_db()
        self.assertEqual(response.data, ActionSerializer(instance=action).data)
        self.assertEqual(action.name, new_name)
        self.assertEqual(action.description, new_description)

    def test_delete_action_204_NO_CONTENT(self):
        action: Action = ActionFactory()
        self.assertEqual(Action.objects.count(), 1)
        self.url = reverse('core:action', kwargs={'uuid': action.uuid.hex})
        response = self.client.delete(self.url)
        self.assertEqual(Action.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
