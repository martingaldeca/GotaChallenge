from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from core.api.serializers import ActionSerializer
from core.models import Action


class ActionListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ActionSerializer
    queryset = Action.objects.all()


class CreateNewActionView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ActionSerializer


class RetrieveUpdateDestroyActionView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ActionSerializer
    queryset = Action.objects.all()

    lookup_url_kwarg = 'uuid'
    lookup_field = 'uuid'
