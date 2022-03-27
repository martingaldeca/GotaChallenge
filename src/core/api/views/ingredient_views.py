from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from core.api.serializers import IngredientSerializer
from core.models import Ingredient


class IngredientListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class CreateNewIngredientView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = IngredientSerializer


class RetrieveUpdateDestroyIngredientView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

    lookup_url_kwarg = 'uuid'
    lookup_field = 'uuid'
