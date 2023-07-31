import random

from django.core.files.base import ContentFile
from factory import SubFactory, LazyAttribute, Sequence
from factory import post_generation
from factory.django import DjangoModelFactory, ImageField
from factory.fuzzy import FuzzyText, FuzzyFloat

from core.factories import DeviceFactory, ActionFactory, IngredientFactory
from core.models import RecipyStep


class RecipyStepFactory(DjangoModelFactory):
    class Meta:
        model = RecipyStep

    name = FuzzyText()
    description = FuzzyText()
    action = LazyAttribute(
        lambda recipy_step: recipy_step.device.allowed_actions.last()
    )
    device = SubFactory(DeviceFactory)
    time = FuzzyFloat(low=0, high=60 * 24 * 7, precision=2)
    image = LazyAttribute(
        lambda _: ContentFile(
            ImageField()._make_data(
                {'width': 1024, 'height': 768}
            ), 'example.jpg'
        )
    )
    ordinal = Sequence(lambda n: n)

    @post_generation
    def ingredients(self: RecipyStep, create, extracted, **kwargs):
        total_ingredients = kwargs.get('total_ingredients', random.randint(1, 5))
        fixed_quantity = kwargs.get('fixed_quantity', False)
        for _ in range(total_ingredients):
            self.add_ingredient(
                ingredient=IngredientFactory(),
                quantity=(fixed_quantity if fixed_quantity else random.uniform(0.01, 2500))
            )
