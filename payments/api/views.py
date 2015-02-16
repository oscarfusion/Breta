from rest_framework import viewsets
from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.response import Response

from ..models import CreditCard, PayoutMethod
from .serializers import CreditCardSerializer, PayoutMethodSerializer
from .permissions import CreditCardPermissions, PayoutMethodPermissions
from .forms import CreateCreditCardForm
from .. import stripe_api


class CreditCardViewSet(viewsets.ModelViewSet):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer
    permission_classes = (CreditCardPermissions, )

    def get_queryset(self, *args, **kwargs):
        return CreditCard.objects.filter(customer__user=self.request.user).all()

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


class PayoutMethodViewSet(viewsets.ModelViewSet):
    queryset = PayoutMethod.objects.all()
    serializer_class = PayoutMethodSerializer
    permission_classes = (PayoutMethodPermissions, )

    def get_queryset(self, *args, **kwargs):
        return PayoutMethod.objects.filter(user=self.request.user).all()

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        recipient = stripe_api.create_recipient(self.request.data.get('stripeToken'), self.request.data['name'], self.request.user.email)
        instance.stripe_recipient_id = recipient.id
        instance.extra_data = recipient.to_dict()
        instance.save()
        return instance
