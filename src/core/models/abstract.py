"""
Create here only abstract models that could be used along all the modules of the application.
"""
import uuid

from django.db import models
from django.db.models import QuerySet
from django.db.models import UUIDField
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from core.helpers.handle_storage import handle_storage


class UUIDModel(models.Model):
    uuid = UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class TimeStampedUUIDModel(UUIDModel, TimeStampedModel):
    class Meta:
        abstract = True


class NameAndDescriptionModel(models.Model):
    name = models.CharField(
        max_length=64,
        verbose_name=_('Name'),
    )
    description = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name=_('Description')
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class ActiveModel(models.Model):
    active = models.BooleanField(
        null=True,
        blank=True,
        verbose_name=_('Active'),
        help_text=_('Field that shows if the model is active(True) or deactivated (False)')
    )

    class Meta:
        abstract = True

    class QuerySet(QuerySet):

        @property
        def active(self):
            return self.filter(active=True)

        @property
        def deactivated(self):
            return self.filter(active=False)

    @property
    def is_active(self):
        return self.active

    @property
    def is_deactivated(self):
        return not self.active

    def activate(self):
        self.active = True
        return self.save()

    def deactivate(self):
        self.active = False
        return self.save()


class ImageModel(models.Model):
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=handle_storage,
        verbose_name=_('Image')
    )

    class Meta:
        abstract = True
