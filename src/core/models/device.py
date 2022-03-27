from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedUUIDModel, NameAndDescriptionModel, Action, ActiveModel, ImageModel
from core.querysets import DeviceQuerySet, DeviceActionRelationshipQuerySet


class DeviceActionRelationship(ActiveModel):
    device = models.ForeignKey('Device', on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)

    objects = models.Manager.from_queryset(DeviceActionRelationshipQuerySet)()

    class Meta:
        verbose_name = _('Device action relation')
        verbose_name_plural = _('Device action relations')


class Device(TimeStampedUUIDModel, NameAndDescriptionModel, ActiveModel, ImageModel):
    allowed_actions = models.ManyToManyField(
        Action,
        blank=True,
        through=DeviceActionRelationship,
        related_name='allowed_actions',
        verbose_name=_('Allowed actions'),
        help_text=_(
            'Allowed actions for the device. The actions can be active or not, you can check '
            'that info looking the through model.'
        )
    )
    objects = models.Manager.from_queryset(DeviceQuerySet)()

    class Meta:
        verbose_name = _('Device')
        verbose_name_plural = _('Devices')

    def add_action(self, action: Action, active: bool = True):
        DeviceActionRelationship.objects.create(device=self, action=action, active=active)

    @property
    def active_actions(self):
        return Action.objects.filter(
            id__in=DeviceActionRelationship.objects.filter(device=self).active.values_list('action')
        )

    @property
    def deactivated_actions(self):
        return Action.objects.filter(
            id__in=DeviceActionRelationship.objects.filter(device=self).deactivated.values_list('action')
        )
