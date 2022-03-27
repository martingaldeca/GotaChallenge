from django.db.models import QuerySet, Count, F, Case, When, IntegerField


class RecipyQuerySet(QuerySet):

    @property
    def with_total_ingredients(self):
        return self.annotate(
            total_ingredients=Count(
                F('recipy_steps__ingredients')
            )
        )

    @property
    def with_total_vegetarian_ingredients(self):
        from core.models import Ingredient
        return self.annotate(
            total_vegetarian_ingredients=Count(
                Case(
                    When(
                        recipy_steps__ingredients__food_type__in=Ingredient.VEGETARIAN_FOOD_TYPES,
                        then=1
                    ),
                    output_field=IntegerField()
                )
            )
        )

    @property
    def with_total_vegan_ingredients(self):
        from core.models import Ingredient
        return self.annotate(
            total_vegan_ingredients=Count(
                Case(
                    When(
                        recipy_steps__ingredients__food_type__in=Ingredient.VEGAN_FOOD_TYPES,
                        then=1
                    ),
                    output_field=IntegerField()
                )
            )
        )

    @property
    def vegetarian(self):
        return self.with_total_ingredients.with_total_vegetarian_ingredients.filter(
            total_ingredients=F('total_vegetarian_ingredients')
        )

    @property
    def vegan(self):
        return self.with_total_ingredients.with_total_vegan_ingredients.filter(
            total_ingredients=F('total_vegan_ingredients')
        )
