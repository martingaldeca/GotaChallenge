from django.db.models import QuerySet


class RecipyStepQuerySet(QuerySet):
    @property
    def device_required(self):
        return self.filter(device__isnull=False)

    @property
    def ordered(self):
        return self.order_by('ordinal')
