from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedUUIDModel, NameAndDescriptionModel, ImageModel, Ingredient, Device, Action
from core.querysets import RecipyStepQuerySet


class StepIngredientRelationShip(TimeStampedUUIDModel):
    recipy_step = models.ForeignKey('RecipyStep', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    quantity = models.FloatField(
        verbose_name=_('Quantity'),
        help_text=_(
            'The quantity required for the recipy step. All will be in gr.'
        )
    )


class RecipyStep(TimeStampedUUIDModel, NameAndDescriptionModel, ImageModel):
    ingredients = models.ManyToManyField(
        Ingredient,
        through=StepIngredientRelationShip,
        related_name='recipy_steps',
        verbose_name=_('Ingredients'),
        help_text=_(
            'All the needed ingredients in the recipy step'
        )
    )
    device = models.ForeignKey(
        Device,
        null=True,
        blank=True,
        verbose_name=_('Device'),
        help_text=_(
            'The device to use in the recipy step. Only one device per step is allowed. '
            'If the step does not require any device it will be None.'
        ),
        on_delete=models.SET_NULL,
        related_name='recipy_steps',
    )
    action = models.ForeignKey(
        Action,
        verbose_name=_('Action'),
        help_text=_(
            'The action to use in the recipy step. Only one action per step is allowed. '
            'All the recipy steps will require an action.'
        ),
        on_delete=models.PROTECT,
        related_name='recipy_steps',
    )
    time = models.FloatField(
        verbose_name=_('Time'),
        help_text=_(
            'Time required to complete the recipy step. All Recipy steps must have a defined time. '
            'All the times are in seconds'
        )
    )
    ordinal = models.IntegerField(
        verbose_name=_('Ordinal'),
        help_text=_('The ordinal number of the step in the recipy'),
        null=True,
        blank=True,
    )

    objects = models.Manager.from_queryset(RecipyStepQuerySet)()

    class Meta:
        verbose_name = _('Recipy step')
        verbose_name_plural = _('Recipy steps')

    def save(self, *args, **kwargs):
        if self.device and self.action not in self.device.allowed_actions.all():
            raise ValueError('Action not allowed for the device.')
        if self.time < 0.0:
            raise ValueError('Time of action must be positive or 0.')
        super(RecipyStep, self).save(*args, **kwargs)

    @property
    def require_device(self):
        return bool(self.device)

    @property
    def ingredients_with_quantities(self):
        id_list = list(
            StepIngredientRelationShip.objects.filter(
                recipy_step=self
            ).order_by(
                'ingredient__name'
            ).prefetch_related(
                'ingredient'
            ).values_list('ingredient__id', 'quantity')
        )
        ingredients_with_quantities = []
        for id, quantity in id_list:
            ingredients_with_quantities.append([Ingredient.objects.get(id=id), quantity])
        return ingredients_with_quantities

    def add_ingredient(self, ingredient: Ingredient, quantity: float):
        StepIngredientRelationShip.objects.create(recipy_step=self, ingredient=ingredient, quantity=quantity)
