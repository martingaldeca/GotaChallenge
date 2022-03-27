from django.test import TestCase

from core.factories import RecipyStepFactory, ActionFactory, IngredientFactory
from core.models import RecipyStep


class RecipyStepTest(TestCase):
    def test_action_not_allowed(self):
        recipy_step: RecipyStep = RecipyStepFactory()
        recipy_step.action = ActionFactory()
        with self.assertRaises(ValueError) as expected_exception:
            recipy_step.save()
        self.assertEqual(str(expected_exception.exception), 'Action not allowed for the device.')

    def test_time_not_allowed(self):
        recipy_step: RecipyStep = RecipyStepFactory()
        recipy_step.time = -1.0
        with self.assertRaises(ValueError) as expected_exception:
            recipy_step.save()
        self.assertEqual(str(expected_exception.exception), 'Time of action must be positive or 0.')

    def test_require_device(self):
        recipy_step: RecipyStep = RecipyStepFactory()
        self.assertEqual(RecipyStep.objects.all().device_required.count(), 1)
        self.assertTrue(recipy_step.require_device)
        recipy_step.device = None
        recipy_step.save()
        self.assertEqual(RecipyStep.objects.all().device_required.count(), 0)
        self.assertFalse(recipy_step.require_device)

    def test_ingredients_with_quantities(self):
        recipy_step: RecipyStep = RecipyStepFactory(ingredients__total_ingredients=3, ingredients__fixed_quantity=1.0)
        ingredients = list(recipy_step.ingredients.order_by('name'))
        expected = [(ingredient.name, 1.0) for ingredient in ingredients]
        self.assertEqual(recipy_step.ingredients_with_quantities, expected)

    def test_add_ingredient(self):
        recipy_step: RecipyStep = RecipyStepFactory(ingredients__total_ingredients=0)
        self.assertEqual(recipy_step.ingredients.count(), 0)
        recipy_step.add_ingredient(ingredient=IngredientFactory(), quantity=1.0)
        self.assertEqual(recipy_step.ingredients.count(), 1)
