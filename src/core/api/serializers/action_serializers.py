from rest_framework import serializers

from core.models import Action


class ActionSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex', read_only=True)

    class Meta:
        model = Action
        fields = ['uuid', 'name', 'description', ]
