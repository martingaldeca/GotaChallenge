from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedUUIDModel, NameAndDescriptionModel, ImageModel, RecipyStep, Ingredient
from core.querysets import RecipyQuerySet


class Recipy(TimeStampedUUIDModel, NameAndDescriptionModel, ImageModel):
    recipy_steps = models.ManyToManyField(
        RecipyStep,
        verbose_name=_('Recipy steps'),
        help_text=_('All the recipy steps to follow in order to complete the recipy.'),
    )

    objects = models.Manager.from_queryset(RecipyQuerySet)()

    class Meta:
        verbose_name = _('Recipy')
        verbose_name_plural = _('Recipies')

    def add_recipy_step(
            self,
            name,
            ingredients_with_quantities,
            action,
            time,
            device=None,
            ordinal=None,
            description=None,
            image=None
    ):
        if not ordinal:
            ordinal = self.recipy_steps.count()
        recipy_step = RecipyStep.objects.create(
            name=name,
            description=description,
            action=action,
            device=device,
            time=time,
            ordinal=ordinal,
            image=image,
        )
        for ingredient, quantity in ingredients_with_quantities:
            recipy_step.add_ingredient(ingredient=ingredient, quantity=quantity)
        self.recipy_steps.add(recipy_step)

    @property
    def ingredients(self):
        return Ingredient.objects.filter(id__in=self.recipy_steps.all().values_list('ingredients', flat=True))

    @property
    def is_vegetarian(self):
        return self.ingredients.all().vegetarian.count() == self.ingredients.all().count()

    @property
    def is_vegan(self):
        return self.ingredients.all().vegan.count() == self.ingredients.all().count()

    @property
    def total_calories(self):
        return sum(
            ingredient.calories
            for ingredient in self.ingredients
            if ingredient.price
        )

    @property
    def total_price(self):
        return sum(
            ingredient.price
            for ingredient in self.ingredients
            if ingredient.calories
        )

    @property
    def total_time(self):
        return sum(self.recipy_steps.values_list('time', flat=True))

    @property
    def total_steps(self):
        return self.recipy_steps.count()

    @property
    def total_ingredients(self):
        return self.ingredients.count()
