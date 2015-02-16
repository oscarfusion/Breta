from rest_framework import viewsets
from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.response import Response

from ..models import CreditCard, Customer
from .serializers import CreditCardSerializer
from .permissions import CreditCardPermissions
from .forms import CreateCreditCardForm


class CreditCardViewSet(viewsets.ModelViewSet):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer
    permission_classes = (CreditCardPermissions, )

    def get_queryset(self, *args, **kwargs):
        try:
            return CreditCard.objects.filter(customer=self.request.user.stripe_customer).all()
        except Customer.DoesNotExist:
            return CreditCard.objects.none()

    def perform_create(self, serializer):
        form = CreateCreditCardForm(self.request.data)
        if not form.is_valid():
            raise PermissionDenied()  # TODO: Fix me to return 400 with proper errors
        return form.save(self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        serializer.instance = obj
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
