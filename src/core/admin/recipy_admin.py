from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from core.models import Recipy


@admin.register(Recipy)
class RecipyAdmin(admin.ModelAdmin):
    search_fields = (
        'uuid', 'id', 'name',
    )
    readonly_fields = [
        'get_image', 'get_total_steps', 'get_total_time',
        'get_total_price', 'get_total_calories', 'get_is_vegetarian', 'get_is_vegan', 'get_total_ingredients'
    ]
    raw_id_fields = ['recipy_steps', ]
    list_display = (
        'id', 'uuid', 'name', 'get_total_steps', 'get_total_time',
        'get_total_price', 'get_total_calories', 'get_is_vegetarian', 'get_is_vegan', 'get_total_ingredients'
    )

    def get_image(self, obj: Recipy):
        return format_html(f'<ul><li><img src="{obj.image.url}" width="auto" height="200px" /></li></ul>')

    get_image.short_description = _('Rendered image')

    def get_total_steps(self, obj: Recipy):
        return obj.total_steps

    get_total_steps.short_description = _('Total steps')

    def get_total_time(self, obj: Recipy):
        return obj.total_time

    get_total_time.short_description = _('Total time')

    def get_total_price(self, obj: Recipy):
        return obj.total_price

    get_total_price.short_description = _('Total price')

    def get_total_calories(self, obj: Recipy):
        return obj.total_calories

    get_total_calories.short_description = _('Total calories')

    def get_is_vegetarian(self, obj: Recipy):
        return obj.is_vegetarian

    get_is_vegetarian.short_description = _('Is vegetarian')
    get_is_vegetarian.boolean = True

    def get_is_vegan(self, obj: Recipy):
        return obj.is_vegan

    get_is_vegan.short_description = _('Is vegan')
    get_is_vegan.boolean = True

    def get_total_ingredients(self, obj: Recipy):
        return obj.total_ingredients

    get_total_ingredients.short_description = _('Total ingredients')
