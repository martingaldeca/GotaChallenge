import uuid

from django.test import TestCase

from core.api.serializers import (
    RecipyStepSerializer, ActionSerializer, DeviceSerializer, IngredientSerializer, UpdateRecipyStepSerializer
)
from core.exceptions import api as api_exceptions
from core.factories import RecipyStepFactory
from core.models import RecipyStep, Ingredient


class RecipyStepSerializerTest(TestCase):

    def test_data(self):
        fixed_quantity = 5.0
        recipy_step: RecipyStep = RecipyStepFactory(
            ingredients__total_ingredients=1,
            ingredients__fixed_quantity=fixed_quantity
        )
        ingredient = Ingredient.objects.last()
        expected_data = {
            'uuid': recipy_step.uuid.hex,
            'name': recipy_step.name,
            'description': recipy_step.description,
            'ingredients': [
                {
                    'ingredient': IngredientSerializer(ingredient).data,
                    'quantity': fixed_quantity,
                }
            ],
            'device': DeviceSerializer(recipy_step.device).data,
            'action': ActionSerializer(recipy_step.action).data,
            'time': recipy_step.time,
            'ordinal': recipy_step.ordinal,
        }
        self.assertEqual(RecipyStepSerializer(recipy_step).data, expected_data)


class UpdateRecipyStepSerializerTest(TestCase):

    def test_not_valid_device(self):
        data = {
            'device': uuid.uuid4().hex,
        }
        serializer = UpdateRecipyStepSerializer(data=data)
        with self.assertRaises(api_exceptions.NotFoundException) as expected_exception:
            serializer.is_valid(raise_exception=True)

        self.assertEqual(expected_exception.exception.detail['message'], 'device-not-found')

    def test_not_valid_action(self):
        data = {
            'action': uuid.uuid4().hex,
        }
        serializer = UpdateRecipyStepSerializer(data=data)
        with self.assertRaises(api_exceptions.NotFoundException) as expected_exception:
            serializer.is_valid(raise_exception=True)

        self.assertEqual(expected_exception.exception.detail['message'], 'action-not-found')
