from django.core.exceptions import PermissionDenied
from django.db.models import Q
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from stripe.error import StripeError

from ..models import CreditCard, PayoutMethod, Transaction
from .serializers import CreditCardSerializer, PayoutMethodSerializer, TransactionSerializer
from .permissions import CreditCardPermissions, PayoutMethodPermissions, TransactionPermissions
from .forms import CreateCreditCardForm
from .. import stripe_api
from .. import bl
from .. import email
from .. import utils


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
        try:
            obj = self.perform_create(serializer)
        except StripeError as e:
            return Response({'stripeToken': e.message}, status=status.HTTP_400_BAD_REQUEST)
        email.send_new_payment_method_email(obj)
        serializer.instance = obj
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PayoutMethodViewSet(viewsets.ModelViewSet):
    queryset = PayoutMethod.objects.all()
    serializer_class = PayoutMethodSerializer
    permission_classes = (PayoutMethodPermissions, )

    def get_queryset(self, *args, **kwargs):
        return PayoutMethod.objects.filter(user=self.request.user).all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            obj = self.perform_create(serializer)
        except StripeError as e:
            return Response({e.json_body['error']['param']: e.message}, status=status.HTTP_400_BAD_REQUEST)
        email.send_new_payout_method_email(obj)
        serializer.instance = obj
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        recipient = stripe_api.create_recipient(self.request.data.get('stripeToken'), self.request.data.get('name'), self.request.user.email)
        instance = serializer.save(user=self.request.user)
        instance.stripe_recipient_id = recipient.id
        instance.extra_data = recipient.to_dict()
        instance.save()
        return instance


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (TransactionPermissions, )

    def get_queryset(self, *args, **kwargs):
        return Transaction.objects.select_related('milestone', 'milestone__project').filter(
            Q(credit_card__customer__user=self.request.user) |
            Q(payer=self.request.user) |
            Q(receiver=self.request.user) |
            Q(payout_method__user=self.request.user)
        )

    def filter_queryset(self, queryset):
        return utils.get_visible_transactions(self.request.user, queryset)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            obj = self.perform_create(serializer)
        except StripeError as e:
            return Response({'credit_card': e.message}, status=status.HTTP_400_BAD_REQUEST)
        if obj is not None:
            serializer.instance = obj
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({
            'success': True
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        instance = bl.create_transaction(self.request.data.get('credit_card'), self.request.user, self.request.data.get('amount'), self.request.data['transaction_type'], self.request.data.get('milestone'))
        return instance


class UsersBalancesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = None
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def retrieve(self, request, pk=None):
        data = None
        if pk == 'me':
            data = {
                'userBalance': {
                    'id': 'me',
                    'balance': str(bl.get_user_balance(self.request.user.id))
                }
            }
        return Response(data)


class UserHasActiveCreditCardViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = None
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def list(self, request, *args, **kwargs):
        try:
            method = CreditCard.objects.select_related().get(
                customer__user=request.user,
                is_active=True
            )
        except CreditCard.DoesNotExist:
            method = None
        res_data = {
            'hasCard': method is not None,
            'isDeveloper': request.user.developer.first() is not None
        }
        return Response(res_data, status=status.HTTP_200_OK)
