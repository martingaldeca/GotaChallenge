from django.contrib import admin

from core.models import Action


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    search_fields = (
        'uuid', 'id', 'name',
    )
    list_display = ('id', 'uuid', 'name')
