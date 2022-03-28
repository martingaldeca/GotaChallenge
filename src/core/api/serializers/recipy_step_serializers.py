import ast

from django.core import exceptions
from django.db import transaction, models
from rest_framework import serializers

from core.api.serializers import DeviceSerializer, ActionSerializer, IngredientSerializer
from core.exceptions import api as api_exceptions
from core.models import RecipyStep, Device, Action, Ingredient


class RecipyStepSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex', read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    device = DeviceSerializer()
    action = ActionSerializer()
    ordinal = serializers.IntegerField(read_only=True)  # TODO define a logic for update recipy steps easyly

    class Meta:
        model = RecipyStep
        fields = [
            'uuid', 'name', 'description', 'ingredients', 'device', 'action',
            'time', 'ordinal'
        ]

    def get_ingredients(self, obj: RecipyStep):
        ingredients_with_quantities = []
        for ingredient, quantity in obj.ingredients_with_quantities:
            ingredients_with_quantities.append(
                {
                    'ingredient': IngredientSerializer(ingredient, context=self.context).data,
                    'quantity': quantity
                }
            )
        return ingredients_with_quantities


class UpdateRecipyStepSerializer(RecipyStepSerializer):
    ingredients_with_quantities = serializers.ListField(write_only=True, required=False)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    device = serializers.UUIDField(required=False)
    action = serializers.UUIDField(required=False)
    time = serializers.FloatField(required=False)

    class Meta:
        model = RecipyStep
        fields = [
            'uuid', 'name', 'description', 'ingredients', 'device', 'action',
            'time', 'ordinal', 'ingredients_with_quantities'
        ]

    def validate_device(self, value):
        try:
            return Device.objects.get(uuid=value)
        except Device.DoesNotExist:
            raise api_exceptions.NotFoundException('device-not-found')

    def validate_action(self, value):
        try:
            return Action.objects.get(uuid=value)
        except Action.DoesNotExist:
            raise api_exceptions.NotFoundException('action-not-found')

    @transaction.atomic
    def update(self, instance: RecipyStep, validated_data):

        def _get_if_object_exists(uuid, model: models.Model):
            # TODO extract this to a mixin
            try:
                return model.objects.get(uuid=uuid)
            except (model.DoesNotExist, exceptions.ValidationError):
                raise api_exceptions.NotFoundException(f'{model.__name__.lower()}-not-found')

        if ingredients_with_quantities := validated_data.pop('ingredients_with_quantities', None):
            instance.ingredients.clear()

            if type(ingredients_with_quantities[0]) == str:
                ingredients_with_quantities = [ast.literal_eval(value) for value in ingredients_with_quantities]
            ingredients_with_quantities = [
                [
                    _get_if_object_exists(ingredient_uuid, Ingredient), quantity
                ] for ingredient_uuid, quantity in ingredients_with_quantities
            ]
            for ingredient, quantity in ingredients_with_quantities:
                instance.add_ingredient(ingredient=ingredient, quantity=quantity)

        return super(UpdateRecipyStepSerializer, self).update(instance, validated_data)

    @property
    def data(self):
        return RecipyStepSerializer(self.instance, context=self.context).data
