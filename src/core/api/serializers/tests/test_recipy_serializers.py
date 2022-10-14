import uuid

from django.test import TestCase

from core.api.serializers import (
    RecipySerializer, CreateRecipySerializer, RecipyStepSerializer, IngredientSerializer
)
from core.exceptions import api as api_exceptions
from core.factories import RecipyFactory, DeviceFactory, IngredientFactory
from core.models import Recipy, Device, Action


class RecipySerializerTest(TestCase):

    def test_data(self):
        recipy: Recipy = RecipyFactory()
        expected_data = {
            'uuid': recipy.uuid.hex,
            'name': recipy.name,
            'description': recipy.description,
            'recipy_steps': RecipyStepSerializer(recipy.recipy_steps, many=True).data,
            'ingredients': IngredientSerializer(recipy.ingredients, many=True).data,
            'is_vegetarian': recipy.is_vegetarian,
            'is_vegan': recipy.is_vegan,
            'total_calories': recipy.total_calories,
            'total_price': recipy.total_price,
            'total_time': recipy.total_time,
            'total_ingredients': recipy.total_ingredients,
            'image': recipy.image.url,
        }
        self.assertEqual(RecipySerializer(recipy).data, expected_data)


class CreateOrUpdateRecipySerializerTest(TestCase):

    def setUp(self) -> None:
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
        self.data = {
            'name': self.recipy_name,
            'description': self.recipy_description,
            'image': self.recipy_image,
            'recipy_steps': self.recipy_steps
        }

    def test_create(self):
        serializer = CreateRecipySerializer(data=self.data)
        serializer.is_valid()
        recipy = serializer.create(serializer.validated_data)
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

    def test_device_does_not_exists(self):
        self.data['recipy_steps'][0]['device'] = uuid.uuid4().hex
        serializer = CreateRecipySerializer(data=self.data)
        serializer.is_valid()
        with self.assertRaises(api_exceptions.NotFoundException) as expected_exception:
            serializer.create(serializer.validated_data)
        self.assertEqual(expected_exception.exception.detail['message'], 'device-not-found')

    def test_action_does_not_exists(self):
        self.data['recipy_steps'][0]['action'] = uuid.uuid4().hex
        serializer = CreateRecipySerializer(data=self.data)
        serializer.is_valid()
        with self.assertRaises(api_exceptions.NotFoundException) as expected_exception:
            serializer.create(serializer.validated_data)
        self.assertEqual(expected_exception.exception.detail['message'], 'action-not-found')

    def test_ingredient_does_not_exists(self):
        self.data['recipy_steps'][0]['ingredients_with_quantities'][0][0] = uuid.uuid4().hex
        serializer = CreateRecipySerializer(data=self.data)
        serializer.is_valid()
        with self.assertRaises(api_exceptions.NotFoundException) as expected_exception:
            serializer.create(serializer.validated_data)
        self.assertEqual(expected_exception.exception.detail['message'], 'ingredient-not-found')
