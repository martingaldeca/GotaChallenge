from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedUUIDModel, NameAndDescriptionModel


class Action(TimeStampedUUIDModel, NameAndDescriptionModel):
    class Meta:
        verbose_name = _('Action')
        verbose_name_plural = _('Actions')
