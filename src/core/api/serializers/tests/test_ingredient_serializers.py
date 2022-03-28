import random

import factory
from django.core.files.base import ContentFile
from django.test import TestCase

from core.api.serializers import IngredientSerializer
from core.models import Ingredient


class IngredientSerializerTest(TestCase):

    def setUp(self) -> None:
        self.ingredient_name = 'test_name'
        self.ingredient_description = 'test_description'
        self.ingredient_food_type = Ingredient.VEGAN_FOOD_TYPES[0]
        self.ingredient_calories = random.uniform(0.01, 2500)
        self.ingredient_price = random.uniform(0.01, 2500)
        self.ingredient_image = ContentFile(
            factory.django.ImageField()._make_data(
                {'width': 1024, 'height': 768}
            ), 'example.jpg'
        )

    def test_data(self):
        data = {
            'name': self.ingredient_name,
            'description': self.ingredient_description,
            'food_type': self.ingredient_food_type,
            'calories': self.ingredient_calories,
            'price': self.ingredient_price,
            'image': self.ingredient_image,
        }
        serializer = IngredientSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.assertEqual(Ingredient.objects.count(), 0)
        serializer.save()
        self.assertEqual(Ingredient.objects.count(), 1)
        ingredient = Ingredient.objects.last()
        self.assertEqual(ingredient.name, self.ingredient_name)
        self.assertEqual(ingredient.description, self.ingredient_description)
        self.assertEqual(ingredient.food_type, self.ingredient_food_type)
        self.assertEqual(ingredient.calories, self.ingredient_calories)
        self.assertEqual(ingredient.price, self.ingredient_price)
        self.assertTrue(ingredient.is_vegan)
        self.assertTrue(ingredient.is_vegetarian)

        expected = {
            'uuid': ingredient.uuid.hex,
            'name': ingredient.name,
            'description': ingredient.description,
            'food_type': ingredient.food_type,
            'calories': ingredient.calories,
            'price': ingredient.price,
            'is_vegetarian': ingredient.is_vegetarian,
            'is_vegan': ingredient.is_vegan,
            'image': ingredient.image.url,
        }
        self.assertEqual(serializer.data, expected)
