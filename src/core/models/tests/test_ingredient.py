import random

from django.test import TestCase

from core.factories import IngredientFactory
from core.models import Ingredient


class IngredientTest(TestCase):
    def test_vegetarian_ingredient(self):
        ingredient: Ingredient = IngredientFactory(food_type=Ingredient.T_MEAT)
        self.assertFalse(ingredient.is_vegetarian)
        self.assertEqual(Ingredient.objects.all().vegetarian.count(), 0)
        ingredient: Ingredient = IngredientFactory(food_type=random.choice(Ingredient.VEGETARIAN_FOOD_TYPES))
        self.assertTrue(ingredient.is_vegetarian)
        self.assertEqual(Ingredient.objects.all().vegetarian.count(), 1)

    def test_vegan_ingredient(self):
        ingredient: Ingredient = IngredientFactory(food_type=Ingredient.T_MEAT)
        self.assertFalse(ingredient.is_vegan)
        self.assertEqual(Ingredient.objects.all().vegan.count(), 0)
        ingredient: Ingredient = IngredientFactory(food_type=random.choice(Ingredient.VEGAN_FOOD_TYPES))
        self.assertTrue(ingredient.is_vegan)
        self.assertEqual(Ingredient.objects.all().vegan.count(), 1)

    def test_not_valid_ingredient(self):
        ingredient: Ingredient = IngredientFactory()
        ingredient.food_type = 'not_valid'
        with self.assertRaises(ValueError) as expected_exception:
            ingredient.save()
        self.assertEqual(str(expected_exception.exception), 'Not valid food type.')
