from django.test import TestCase

from core.api.serializers import RecipyStepSerializer, ActionSerializer, DeviceSerializer, IngredientSerializer
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
