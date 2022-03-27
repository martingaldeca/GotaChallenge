from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from core.models import RecipyStep


class IngredientsInline(admin.TabularInline):
    model = RecipyStep.ingredients.through


@admin.register(RecipyStep)
class RecipyStepAdmin(admin.ModelAdmin):
    search_fields = (
        'uuid', 'id', 'name',
    )
    list_filter = ('ingredients__food_type', 'ordinal')
    readonly_fields = ['get_image', ]
    raw_id_fields = ['device', 'action']
    list_display = ('id', 'uuid', 'name', 'device', 'action', 'time', 'ordinal')
    inlines = [IngredientsInline, ]

    def get_image(self, obj: RecipyStep):
        return format_html(f'<ul><li><img src="{obj.image.url}" width="auto" height="200px" /></li></ul>')

    get_image.short_description = _('Rendered image')
