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


class TransactionApiTestCase(APITestCase):
    def test_list_should_return_401_for_non_auth_user(self):
        response = self.client.get(reverse('transaction-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_details_should_return_401_for_non_auth_user(self):
        transaction = TransactionFactory()
        response = self.client.get(reverse('transaction-detail', args=(transaction.id, )))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_list_user_transactions(self):
        TransactionFactory()
        transaction = TransactionFactory()
        user = transaction.credit_card.customer.user
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse('creditcard-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total'], 1)

    def test_should_open_details_for_user_transaction(self):
        transaction = TransactionFactory()
        user = transaction.credit_card.customer.user
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse('transaction-detail', args=(transaction.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_not_open_details_for_not_user_transaction(self):
        another_transaction = TransactionFactory()
        transaction = TransactionFactory()
        user = transaction.credit_card.customer.user
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse('transaction-detail', args=(another_transaction.id, )))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('payments.stripe_api.create_transaction', lambda *a, **k: stripe_transaction)
    def test_should_create_transaction(self):
        card = CreditCardFactory()
        user = card.customer.user
        self.client.force_authenticate(user=user)
        url = reverse('transaction-list')
        data = {
            'credit_card': card.id,
            'transaction_type': Transaction.ESCROW,
            'amount': '100',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        transaction = Transaction.objects.filter(credit_card__customer__user=user).get()
        self.assertEqual(transaction.stripe_id, 'transaction_id')

    @patch('payments.stripe_api.create_transaction')
    def test_should_return_stripe_errors(self, create_transaction):
        def raise_stripe_error(*args, **kwargs):
            raise StripeError(message='test error')
        create_transaction.side_effect = raise_stripe_error
        card = CreditCardFactory()
        user = card.customer.user
        self.client.force_authenticate(user=user)
        url = reverse('transaction-list')
        data = {
            'credit_card': card.id,
            'transaction_type': Transaction.ESCROW,
            'amount': '100',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['credit_card'], 'test error')

        self.assertEqual(Transaction.objects.count(), 0)

    def test_should_now_allow_to_pay_with_not_own_credit_card(self):
        user = UserFactory()
        card = CreditCardFactory()
        self.client.force_authenticate(user=user)
        url = reverse('transaction-list')
        data = {
            'credit_card': card.id,
            'transaction_type': Transaction.ESCROW,
            'amount': '100',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
