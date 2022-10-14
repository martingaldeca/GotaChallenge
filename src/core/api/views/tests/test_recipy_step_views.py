import uuid

from django.urls import reverse
from rest_framework import status

from core.api.serializers import UpdateRecipyStepSerializer
from core.api.views.tests.base import APITestBase
from core.factories import RecipyStepFactory, ActionFactory, DeviceFactory, IngredientFactory
from core.models import RecipyStep, Device, Action


class RetrieveUpdateDestroyRecipyStepViewTest(APITestBase):
    url = reverse('core:recipy-step', kwargs={'uuid': None})

    def test_get_recipy_step_200_OK(self):
        recipy_step: RecipyStep = RecipyStepFactory()
        self.url = reverse('core:recipy-step', kwargs={'uuid': recipy_step.uuid.hex})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            UpdateRecipyStepSerializer(instance=recipy_step, context=self.test_context).data
        )

    def test_update_recipy_step_200_OK(self):
        recipy_step: RecipyStep = RecipyStepFactory()
        self.url = reverse('core:recipy-step', kwargs={'uuid': recipy_step.uuid.hex})

        new_name = 'test_name_2'
        new_description = 'test_description_2'
        new_device: Device = DeviceFactory()
        new_action: Action = new_device.allowed_actions.last()
        new_ingredients = [IngredientFactory(), IngredientFactory()]
        fixed_quantity = 1.0
        data = {
            'name': new_name,
            'description': new_description,
            'device': new_device.uuid.hex,
            'action': new_action.uuid.hex,
            'ingredients_with_quantities': [
                [
                    new_ingredients[0].uuid.hex, fixed_quantity
                ],
                [
                    new_ingredients[1].uuid.hex, fixed_quantity
                ]
            ]
        }

        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        recipy_step.refresh_from_db()
        self.assertEqual(
            response.data,
            UpdateRecipyStepSerializer(instance=recipy_step, context=self.test_context).data
        )
        self.assertEqual(recipy_step.name, new_name)
        self.assertEqual(recipy_step.description, new_description)
        self.assertEqual(recipy_step.device, new_device)
        self.assertEqual(recipy_step.action, new_action)
        self.assertEqual(set(recipy_step.ingredients.all()), set(new_ingredients))

    def test_delete_recipy_step_204_NO_CONTENT(self):
        recipy_step: RecipyStep = RecipyStepFactory()
        self.assertEqual(RecipyStep.objects.count(), 1)
        self.url = reverse('core:recipy-step', kwargs={'uuid': recipy_step.uuid.hex})
        response = self.client.delete(self.url)
        self.assertEqual(RecipyStep.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_recipy_step_not_valid_device_404_NOT_FOUND(self):
        recipy_step: RecipyStep = RecipyStepFactory()
        self.url = reverse('core:recipy-step', kwargs={'uuid': recipy_step.uuid.hex})

        new_name = 'test_name_2'
        new_description = 'test_description_2'
        new_action: Action = ActionFactory()
        new_ingredients = [IngredientFactory(), IngredientFactory()]
        fixed_quantity = 1.0
        data = {
            'name': new_name,
            'description': new_description,
            'device': uuid.uuid4().hex,
            'action': new_action.uuid.hex,
            'ingredients_with_quantities': [
                [
                    new_ingredients[0].uuid.hex, fixed_quantity
                ],
                [
                    new_ingredients[1].uuid.hex, fixed_quantity
                ]
            ]
        }

        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_recipy_step_not_valid_action_404_NOT_FOUND(self):
        recipy_step: RecipyStep = RecipyStepFactory()
        self.url = reverse('core:recipy-step', kwargs={'uuid': recipy_step.uuid.hex})

        new_name = 'test_name_2'
        new_description = 'test_description_2'
        new_device: Device = DeviceFactory()
        new_ingredients = [IngredientFactory(), IngredientFactory()]
        fixed_quantity = 1.0
        data = {
            'name': new_name,
            'description': new_description,
            'device': new_device.uuid.hex,
            'action': uuid.uuid4().hex,
            'ingredients_with_quantities': [
                [
                    new_ingredients[0].uuid.hex, fixed_quantity
                ],
                [
                    new_ingredients[1].uuid.hex, fixed_quantity
                ]
            ]
        }

        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
