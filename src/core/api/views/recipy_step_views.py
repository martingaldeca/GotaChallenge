from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from core.api.serializers import UpdateRecipyStepSerializer
from core.models import RecipyStep


class RetrieveUpdateDestroyRecipyStepView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateRecipyStepSerializer
    queryset = RecipyStep.objects.all()

    lookup_url_kwarg = 'uuid'
    lookup_field = 'uuid'
