import ast

from django.core import exceptions
from django.db import models
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from core.api.serializers import RecipyStepSerializer, IngredientSerializer
from core.exceptions import api as api_exceptions
from core.models import Recipy, Action, Device, Ingredient


class RecipySerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex', read_only=True)
    recipy_steps = RecipyStepSerializer(many=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    description = serializers.CharField(required=False)

    class Meta:
        model = Recipy
        fields = [
            'uuid', 'name', 'description', 'recipy_steps', 'ingredients', 'is_vegetarian', 'is_vegan', 'total_calories',
            'total_price', 'total_time', 'total_ingredients', 'image'
        ]


class CreateRecipySerializer(RecipySerializer):
    recipy_steps = serializers.ListField(min_length=1)
    image = Base64ImageField()

    @property
    def data(self):
        return RecipySerializer(self.instance, context=self.context).data

    @transaction.atomic
    def create(self, validated_data):

        def _get_if_object_exists(uuid, model: models.Model):
            try:
                return model.objects.get(uuid=uuid)
            except (model.DoesNotExist, exceptions.ValidationError):
                raise api_exceptions.NotFoundException(f'{model.__name__.lower()}-not-found')

        # Create the recipy
        recipy = Recipy.objects.create(
            name=validated_data['name'],
            description=validated_data.get('description'),
            image=validated_data.get('image'),
        )

        # Add all the recipy steps
        for recipy_step in validated_data['recipy_steps']:
            if type(recipy_step) == str:
                recipy_step = ast.literal_eval(recipy_step)
            try:
                name = recipy_step['name']
                time = recipy_step['time']
                action = recipy_step['action']
                ingredients_with_quantities = recipy_step['ingredients_with_quantities']
            except KeyError:
                raise api_exceptions.BadRequestException('recipy-step-not-valid')

            description = recipy_step.get('description')
            device = recipy_step.get('device')

            action = _get_if_object_exists(action, Action)

            if device:
                device = _get_if_object_exists(device, Device)

            # Trnasform the ingredients
            ingredients_with_quantities = [
                [
                    _get_if_object_exists(ingredient_uuid, Ingredient), quantity
                ] for ingredient_uuid, quantity in ingredients_with_quantities
            ]

            recipy.add_recipy_step(
                name=name,
                ingredients_with_quantities=ingredients_with_quantities,
                action=action,
                time=time,
                device=device,
                description=description,
            )

        self.instance = recipy
        return recipy
