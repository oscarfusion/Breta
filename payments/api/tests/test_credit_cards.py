from mock import patch, Mock

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from stripe.error import StripeError

from accounts.tests.factories import UserFactory
from payments.tests.factories import CreditCardFactory
from payments.models import CreditCard


stripe_customer = Mock(
    id='customer_id',
    to_dict=lambda: {},
    cards=Mock(data=[Mock(id='card_id', to_dict=lambda: {})])
)


class CreditCardsApiTestCase(APITestCase):
    def test_list_should_return_401_for_non_auth_user(self):
        response = self.client.get(reverse('creditcard-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_details_should_return_401_for_non_auth_user(self):
        credit_card = CreditCardFactory()
        response = self.client.get(reverse('creditcard-detail', args=(credit_card.id, )))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_list_user_cards(self):
        CreditCardFactory()
        credit_card = CreditCardFactory()
        user = credit_card.customer.user
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse('creditcard-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total'], 1)

    def test_should_open_details_for_user_card(self):
        credit_card = CreditCardFactory()
        user = credit_card.customer.user
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse('creditcard-detail', args=(credit_card.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_not_open_details_for_not_user_card(self):
        another_card = CreditCardFactory()
        credit_card = CreditCardFactory()
        user = credit_card.customer.user
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse('creditcard-detail', args=(another_card.id, )))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('payments.stripe_api.create_customer', lambda *a, **k: stripe_customer)
    def test_should_create_credit_card(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        url = reverse('creditcard-list')
        data = {
            'stripeToken': '123456',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        credit_card = CreditCard.objects.filter(customer__user=user).get()
        self.assertEqual(credit_card.stripe_card_id, 'card_id')

    def test_should_require_stripe_token(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        url = reverse('creditcard-list')
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch('payments.stripe_api.create_customer')
    def test_should_return_stripe_errors(self, create_customer):
        def raise_stripe_error(*args, **kwargs):
            raise StripeError(message='test error')
        create_customer.side_effect = raise_stripe_error
        user = UserFactory()
        self.client.force_authenticate(user=user)
        url = reverse('creditcard-list')
        data = {
            'stripeToken': '123456',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['stripeToken'], 'test error')

        self.assertEqual(CreditCard.objects.count(), 0)
