from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedUUIDModel, NameAndDescriptionModel, ImageModel
from core.querysets import IngredientQuerySet


class Ingredient(TimeStampedUUIDModel, NameAndDescriptionModel, ImageModel):
    (
        T_FRUIT, T_VEGETABLE, T_MEAT, T_FISH, T_CEREAL, T_LEGUME, T_NUT, T_TUBER, T_DAIRY, T_EGG
    ) = (
        'fruit', 'vegetable', 'meat', 'fish', 'cereal', 'legume', 'nut', 'tuber', 'dairy', 'egg'
    )
    VEGETARIAN_FOOD_TYPES = [T_FRUIT, T_VEGETABLE, T_CEREAL, T_LEGUME, T_NUT, T_TUBER, T_DAIRY, T_EGG]
    VEGAN_FOOD_TYPES = [T_FRUIT, T_VEGETABLE, T_CEREAL, T_LEGUME, T_NUT, T_TUBER]
    FOOD_TYPES = (
        (T_FRUIT, 'Fruit'),
        (T_VEGETABLE, 'Vegetable'),
        (T_MEAT, 'Meat'),
        (T_FISH, 'Fish'),
        (T_CEREAL, 'Cereal'),
        (T_LEGUME, 'Legume'),
        (T_NUT, 'Nut'),
        (T_TUBER, 'Tuber'),
        (T_DAIRY, 'Dairy'),
        (T_EGG, 'Egg'),
    )
    food_type = models.CharField(
        max_length=20,
        choices=FOOD_TYPES,
        blank=True,
        null=True,
        verbose_name=_('Food type'),
        db_index=True,
    )
    calories = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Calories'),
        help_text=_('Calories of the ingredient for each 100 gr of it')
    )

    # TODO in first version we will suppose that the units of the price is always the same.
    #  In the future we can use a converter service for example
    price = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Price')
    )

    objects = models.Manager.from_queryset(IngredientQuerySet)()

    class Meta:
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')

    def save(self, *args, **kwargs):
        if self.food_type not in [food_type[0] for food_type in Ingredient.FOOD_TYPES]:
            raise ValueError('Not valid food type.')
        super(Ingredient, self).save()

    @property
    def is_vegetarian(self):
        return self.food_type in self.VEGETARIAN_FOOD_TYPES

    @property
    def is_vegan(self):
        return self.food_type in self.VEGAN_FOOD_TYPES
