import random

from django.urls import reverse
from rest_framework import status

from core.api.serializers import RecipySerializer, CreateRecipySerializer
from core.api.views.tests.base import APITestBase
from core.factories import RecipyFactory, DeviceFactory, IngredientFactory
from core.models import Recipy, Device, Action


class RecipyListViewTest(APITestBase):
    url = reverse('core:list-recipies')

    def test_get_200_OK(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])
        recipies = [
            RecipySerializer(
                instance=RecipyFactory(), context=self.test_context
            ).data
            for _ in range(random.randint(1, 5))
        ]
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], recipies)


class CreateNewRecipyViewTest(APITestBase):
    url = reverse('core:create-recipy')

    def setUp(self) -> None:
        super(CreateNewRecipyViewTest, self).setUp()
        self.recipy_name = 'test_name'
        self.recipy_description = 'test_description'
        self.recipy_image = (
            'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4'
            '//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='
        )

        self.recipy_step_1_name = 'test_name_1'
        self.recipy_step_1_description = 'test_description_1'
        self.recipy_step_1_time = 1.0
        self.recipy_step_1_device: Device = DeviceFactory()
        self.recipy_step_1_action: Action = self.recipy_step_1_device.allowed_actions.last()
        self.recipy_step_1_ingredients = [IngredientFactory(), IngredientFactory()]
        self.recipy_step_1_quantities = 1.0

        self.recipy_step_2_name = 'test_name_2'
        self.recipy_step_2_description = 'test_description_2'
        self.recipy_step_2_time = 1.0
        self.recipy_step_2_device: Device = DeviceFactory()
        self.recipy_step_2_action: Action = self.recipy_step_2_device.allowed_actions.last()
        self.recipy_step_2_ingredients = [IngredientFactory(), IngredientFactory(), IngredientFactory()]
        self.recipy_step_2_quantities = 1.0
        self.recipy_steps = [
            {
                'name': self.recipy_step_1_name,
                'description': self.recipy_step_1_description,
                'time': self.recipy_step_1_time,
                'action': self.recipy_step_1_action.uuid.hex,
                'device': self.recipy_step_1_device.uuid.hex,
                'ingredients_with_quantities': [
                    [self.recipy_step_1_ingredients[0].uuid.hex, self.recipy_step_1_quantities],
                    [self.recipy_step_1_ingredients[1].uuid.hex, self.recipy_step_1_quantities],
                ]
            },
            {
                'name': self.recipy_step_2_name,
                'description': self.recipy_step_2_description,
                'time': self.recipy_step_2_time,
                'action': self.recipy_step_2_action.uuid.hex,
                'device': self.recipy_step_2_device.uuid.hex,
                'ingredients_with_quantities': [
                    [self.recipy_step_2_ingredients[0].uuid.hex, self.recipy_step_2_quantities],
                    [self.recipy_step_2_ingredients[1].uuid.hex, self.recipy_step_2_quantities],
                    [self.recipy_step_2_ingredients[2].uuid.hex, self.recipy_step_2_quantities],
                ]
            }
        ]
        self.data_to_send = {
            'name': self.recipy_name,
            'description': self.recipy_description,
            'image': self.recipy_image,
            'recipy_steps': self.recipy_steps
        }

    def test_create_new_recipy_201_CREATED(self):
        self.assertEqual(Recipy.objects.count(), 0)
        response = self.client.post(self.url, data=self.data_to_send)
        self.assertEqual(Recipy.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recipy = Recipy.objects.last()
        self.assertEqual(response.data, CreateRecipySerializer(instance=recipy, context=self.test_context).data)
        self.assertEqual(recipy.name, self.recipy_name)
        self.assertEqual(recipy.description, self.recipy_description)
        first_recipy_step = recipy.recipy_steps.get(ordinal=0)
        self.assertEqual(first_recipy_step.name, self.recipy_step_1_name)
        self.assertEqual(first_recipy_step.description, self.recipy_step_1_description)
        self.assertEqual(first_recipy_step.time, self.recipy_step_1_time)
        self.assertEqual(first_recipy_step.action, self.recipy_step_1_action)
        self.assertEqual(first_recipy_step.device, self.recipy_step_1_device)
        self.assertEqual(set(first_recipy_step.ingredients.all()), set(self.recipy_step_1_ingredients))
        second = recipy.recipy_steps.get(ordinal=1)
        self.assertEqual(second.name, self.recipy_step_2_name)
        self.assertEqual(second.description, self.recipy_step_2_description)
        self.assertEqual(second.time, self.recipy_step_2_time)
        self.assertEqual(second.action, self.recipy_step_2_action)
        self.assertEqual(second.device, self.recipy_step_2_device)
        self.assertEqual(set(second.ingredients.all()), set(self.recipy_step_2_ingredients))


class RetrieveDestroyRecipyViewTest(APITestBase):
    url = reverse('core:recipy', kwargs={'uuid': None})

    def test_get_recipy_200_OK(self):
        recipy: Recipy = RecipyFactory()
        self.url = reverse('core:recipy', kwargs={'uuid': recipy.uuid.hex})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, CreateRecipySerializer(instance=recipy, context=self.test_context).data)

    def test_delete_recipy_204_NO_CONTENT(self):
        recipy: Recipy = RecipyFactory()
        self.assertEqual(Recipy.objects.count(), 1)
        self.url = reverse('core:recipy', kwargs={'uuid': recipy.uuid.hex})
        response = self.client.delete(self.url)
        self.assertEqual(Recipy.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
