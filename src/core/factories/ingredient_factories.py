from django.core.files.base import ContentFile
from factory import LazyAttribute
from factory.django import DjangoModelFactory, ImageField
from factory.fuzzy import FuzzyText, FuzzyChoice, FuzzyFloat

from core.models import Ingredient


class IngredientFactory(DjangoModelFactory):
    class Meta:
        model = Ingredient

    name = FuzzyText()
    description = FuzzyText()
    food_type = FuzzyChoice([food_type[0] for food_type in Ingredient.FOOD_TYPES])
    calories = FuzzyFloat(low=0, high=1000, precision=6)
    price = FuzzyFloat(low=0, high=100, precision=6)
    image = LazyAttribute(
        lambda _: ContentFile(
            ImageField()._make_data(
                {'width': 1024, 'height': 768}
            ), 'example.jpg'
        )
    )
