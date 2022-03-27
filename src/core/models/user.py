from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedUUIDModel


class User(AbstractUser, TimeStampedUUIDModel):
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
