import random

from factory import post_generation, LazyAttribute
from django.core.files.base import ContentFile
from factory.django import DjangoModelFactory, ImageField
from factory.fuzzy import FuzzyText

from core.factories import ActionFactory
from core.models import Device


class DeviceFactory(DjangoModelFactory):
    class Meta:
        model = Device

    name = FuzzyText()
    active = True
    description = FuzzyText()
    image = LazyAttribute(
        lambda _: ContentFile(
            ImageField()._make_data(
                {'width': 1024, 'height': 768}
            ), 'example.jpg'
        )
    )

    @post_generation
    def allowed_actions(self: Device, create, extracted, **kwargs):
        total_active = kwargs.get('total_active', random.randint(1, 5))
        total_deactivated = kwargs.get('total_deactivated', random.randint(1, 5))
        for i in range(total_active):
            self.add_action(action=ActionFactory())
        for i in range(total_deactivated):
            self.add_action(action=ActionFactory(), active=False)
