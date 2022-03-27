from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from core.api.serializers import DeviceSerializer, CreateOrUpdateDeviceSerializer
from core.models import Device


class DeviceListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()


class CreateNewDeviceView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateOrUpdateDeviceSerializer


class RetrieveUpdateDestroyDeviceView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateOrUpdateDeviceSerializer
    queryset = Device.objects.all()

    lookup_url_kwarg = 'uuid'
    lookup_field = 'uuid'
