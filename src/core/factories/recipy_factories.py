import random

from django.core.files.base import ContentFile
from factory import LazyAttribute
from factory import post_generation
from factory.django import DjangoModelFactory, ImageField
from factory.fuzzy import FuzzyText, FuzzyChoice, FuzzyFloat

from core.factories import IngredientFactory, DeviceFactory
from core.models import Recipy, Device, Ingredient


class RecipyFactory(DjangoModelFactory):
    class Meta:
        model = Recipy

    name = FuzzyText()
    description = FuzzyText()
    image = LazyAttribute(
        lambda _: ContentFile(
            ImageField()._make_data(
                {'width': 1024, 'height': 768}
            ), 'example.jpg'
        )
    )

    @post_generation
    def recipy_steps(self: Recipy, create, extracted, **kwargs):
        total_steps = kwargs.get('total_steps', random.randint(1, 5))
        food_type = kwargs.get('food_type', FuzzyChoice([food_type[0] for food_type in Ingredient.FOOD_TYPES]))
        fixed_calories = kwargs.get('fixed_calories', FuzzyFloat(low=0, high=1000, precision=6))
        fixed_price = kwargs.get('fixed_price', FuzzyFloat(low=0, high=1000, precision=6))
        fixed_num_of_ingredients = kwargs.get('fixed_num_of_ingredients', random.randint(1, 5))
        fixed_time = kwargs.get('fixed_time', random.uniform(0.01, 2500))
        for i in range(total_steps):
            ingredients_with_quantity = []
            for i in range(fixed_num_of_ingredients):
                ingredients_with_quantity.append(
                    (
                        IngredientFactory(food_type=food_type, calories=fixed_calories, price=fixed_price),
                        random.uniform(0.01, 2500)
                    )
                )

            device: Device = DeviceFactory()
            self.add_recipy_step(
                name=FuzzyText(),
                description=FuzzyText(),
                ingredients_with_quantity=ingredients_with_quantity,
                action=device.allowed_actions.last(),
                time=fixed_time,
                device=device,
            )
