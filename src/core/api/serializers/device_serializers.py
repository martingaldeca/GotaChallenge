from rest_framework import serializers

from core.api.serializers import ActionSerializer
from core.exceptions import api as api_exceptions
from core.models import Device, Action


class DeviceSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex', read_only=True)
    allowed_actions = ActionSerializer(many=True, read_only=True)
    active_actions = ActionSerializer(read_only=True, many=True)
    deactivated_actions = ActionSerializer(read_only=True, many=True)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Device
        fields = [
            'uuid', 'name', 'description', 'allowed_actions', 'image', 'active',
            'deactivated_actions', 'active_actions'
        ]


class CreateOrUpdateDeviceSerializer(DeviceSerializer):
    allowed_actions = serializers.ListField(required=False)

    @staticmethod
    def validate_allowed_actions(value):
        allowed_actions = []
        for uuid in value:
            try:
                allowed_actions.append(Action.objects.get(uuid=uuid))
            except Action.DoesNotExist:
                raise api_exceptions.NotFoundException('action-not-found')
        return allowed_actions

    def create(self, validated_data):
        allowed_actions = self.validated_data.pop('allowed_actions', None)
        device: Device = super(CreateOrUpdateDeviceSerializer, self).create(self.validated_data)

        # Add all the actions
        if allowed_actions:
            for action in allowed_actions:
                device.add_action(action=action)

        self.instance = device
        return device

    @property
    def data(self):
        return DeviceSerializer(self.instance, context=self.context).data
