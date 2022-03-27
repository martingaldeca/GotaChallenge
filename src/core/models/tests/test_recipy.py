from django.test import TestCase

from core.factories import RecipyFactory, ActionFactory, IngredientFactory
from core.models import Recipy, Ingredient


class RecipyTest(TestCase):
    def test_is_vegetarian(self):
        recipy: Recipy = RecipyFactory(recipy_steps__food_type=Ingredient.VEGETARIAN_FOOD_TYPES[0])
        self.assertTrue(recipy.is_vegetarian)
        self.assertEqual(Recipy.objects.all().vegetarian.count(), 1)

        ingredients_with_quantity = [
            (IngredientFactory(food_type=Ingredient.T_MEAT), 1994.0)
        ]
        recipy.add_recipy_step(
            name='test_step',
            description='test_description',
            action=ActionFactory(),
            time=1994.0,
            ingredients_with_quantity=ingredients_with_quantity
        )
        self.assertFalse(recipy.is_vegetarian)
        self.assertEqual(Recipy.objects.all().vegetarian.count(), 0)

    def test_is_vegan(self):
        recipy: Recipy = RecipyFactory(recipy_steps__food_type=Ingredient.VEGAN_FOOD_TYPES[0])
        self.assertTrue(recipy.is_vegan)
        self.assertEqual(Recipy.objects.all().vegan.count(), 1)

        ingredients_with_quantity = [
            (IngredientFactory(food_type=Ingredient.T_EGG), 1994.0)
        ]
        recipy.add_recipy_step(
            name='test_step',
            description='test_description',
            action=ActionFactory(),
            time=1994.0,
            ingredients_with_quantity=ingredients_with_quantity
        )
        self.assertFalse(recipy.is_vegan)
        self.assertEqual(Recipy.objects.all().vegan.count(), 0)

    def test_total_calories(self):
        total_steps = 3
        fixed_num_of_ingredients = 3
        fixed_calories = 1.0
        recipy: Recipy = RecipyFactory(
            recipy_steps__total_steps=total_steps,
            recipy_steps__fixed_num_of_ingredients=fixed_num_of_ingredients,
            recipy_steps__fixed_calories=fixed_calories
        )
        self.assertEqual(recipy.total_calories, total_steps * fixed_num_of_ingredients * fixed_calories)

    def test_total_price(self):
        total_steps = 3
        fixed_num_of_ingredients = 3
        fixed_calories = 1.0
        recipy: Recipy = RecipyFactory(
            recipy_steps__total_steps=total_steps,
            recipy_steps__fixed_num_of_ingredients=fixed_num_of_ingredients,
            recipy_steps__fixed_price=fixed_calories
        )
        self.assertEqual(recipy.total_price, total_steps * fixed_num_of_ingredients * fixed_calories)

    def test_total_time(self):
        total_steps = 3
        fixed_time = 1.0
        recipy: Recipy = RecipyFactory(
            recipy_steps__total_steps=total_steps,
            recipy_steps__fixed_time=fixed_time
        )
        self.assertEqual(recipy.total_time, total_steps * fixed_time)
