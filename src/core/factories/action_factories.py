from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from core.models import Action


class ActionFactory(DjangoModelFactory):
    class Meta:
        model = Action

    name = FuzzyText()
    description = FuzzyText()
