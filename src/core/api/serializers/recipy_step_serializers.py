from rest_framework import serializers

from core.api.serializers import DeviceSerializer, ActionSerializer, IngredientSerializer
from core.models import RecipyStep


class RecipyStepSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex')
    ingredients = serializers.SerializerMethodField()
    device = DeviceSerializer()
    action = ActionSerializer()

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
