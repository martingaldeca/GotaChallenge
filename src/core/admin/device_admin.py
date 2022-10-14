from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from core.models import Device


class ActionsInline(admin.TabularInline):
    model = Device.allowed_actions.through


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    search_fields = (
        'uuid', 'id', 'name'
    )
    readonly_fields = ['get_image', ]
    list_filter = ('active',)
    raw_id_fields = ['allowed_actions']
    list_display = ('id', 'uuid', 'name', 'active')
    inlines = [ActionsInline, ]

    def get_image(self, obj: Device):
        return format_html(f'<ul><li><img src="{obj.image.url}" width="auto" height="200px" /></li></ul>')

    get_image.short_description = _('Rendered image')
