from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from core.api.serializers import RecipySerializer, CreateRecipySerializer
from core.models import Recipy


class RecipyListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RecipySerializer
    queryset = Recipy.objects.all()


class CreateNewRecipyView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateRecipySerializer


class RetrieveUpdateDestroyRecipyView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateRecipySerializer
    queryset = Recipy.objects.all()

    lookup_url_kwarg = 'uuid'
    lookup_field = 'uuid'
