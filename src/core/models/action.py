from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedUUIDModel, NameAndDescriptionModel


class Action(TimeStampedUUIDModel, NameAndDescriptionModel):
    name = models.CharField(
        max_length=64,
        verbose_name=_('Name'),
        unique=True
    )

    class Meta:
        verbose_name = _('Action')
        verbose_name_plural = _('Actions')
