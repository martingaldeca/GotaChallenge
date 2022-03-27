from rest_framework import serializers

from core.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    uuid = uuid = serializers.UUIDField(format='hex', read_only=True)
    is_vegetarian = serializers.BooleanField(read_only=True)
    is_vegan = serializers.BooleanField(read_only=True)

    class Meta:
        model = Ingredient
        fields = [
            'uuid', 'name', 'description', 'food_type', 'calories', 'price',
            'is_vegetarian', 'is_vegan'
        ]
