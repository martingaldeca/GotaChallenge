from rest_framework import serializers

from core.exceptions import api as api_exceptions
from core.models import User


class SimpleUserSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex')

    class Meta:
        model = User
        fields = ['uuid', 'username']


class MeSerializer(SimpleUserSerializer):
    class Meta:
        model = User
        fields = ['uuid', 'username', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    @staticmethod
    def validate_email(value):
        if User.objects.filter(email=value).exists():
            raise api_exceptions.ConflictException('email-not-valid')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    @property
    def data(self):
        return None
