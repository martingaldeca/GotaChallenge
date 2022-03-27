from django.db.models import QuerySet


class IngredientQuerySet(QuerySet):
    @property
    def vegetarian(self):
        from core.models import Ingredient
        return self.filter(food_type__in=Ingredient.VEGETARIAN_FOOD_TYPES)

    @property
    def vegan(self):
        from core.models import Ingredient
        return self.filter(food_type__in=Ingredient.VEGAN_FOOD_TYPES)
