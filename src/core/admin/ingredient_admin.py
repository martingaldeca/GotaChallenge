from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from core.models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = (
        'uuid', 'id', 'name'
    )
    list_filter = ('food_type', )
    readonly_fields = ['get_image', ]
    list_display = ('id', 'uuid', 'name', 'food_type', 'calories', 'price')

    def get_image(self, obj: Ingredient):
        return format_html(f'<ul><li><img src="{obj.image.url}" width="auto" height="200px" /></li></ul>')

    get_image.short_description = _('Rendered image')
