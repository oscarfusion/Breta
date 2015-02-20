from mock import patch, Mock

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from stripe.error import StripeError

from accounts.tests.factories import UserFactory
from payments.tests.factories import CreditCardFactory, TransactionFactory
from payments.models import Transaction


stripe_transaction = Mock(
    id='transaction_id',
    to_dict=lambda: {},
)


class UserBalanceApiTestCase(APITestCase):
    def test_list_should_return_401_for_non_auth_user(self):
        response = self.client.get(reverse('user-balance-detail', args=('me', )))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_return_user_balance(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse('user-balance-detail', args=('me', )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
