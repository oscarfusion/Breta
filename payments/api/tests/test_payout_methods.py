from mock import patch, Mock

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from stripe.error import StripeError

from accounts.tests.factories import UserFactory
from payments.tests.factories import PayoutMethodFactory
from payments.models import PayoutMethod


stripe_recipient = Mock(
    id='recipient_id',
    to_dict=lambda: {},
)


class PayoutMethodApiTestCase(APITestCase):
    def test_list_should_return_401_for_non_auth_user(self):
        response = self.client.get(reverse('payoutmethod-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_details_should_return_401_for_non_auth_user(self):
        payout_method = PayoutMethodFactory()
        response = self.client.get(reverse('payoutmethod-detail', args=(payout_method.id, )))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_list_user_payout_methods(self):
        PayoutMethodFactory()
        payout_method = PayoutMethodFactory()
        user = payout_method.user
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse('payoutmethod-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total'], 1)

    def test_should_open_details_for_user_payout_method(self):
        payout_method = PayoutMethodFactory()
        user = payout_method.user
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse('payoutmethod-detail', args=(payout_method.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_not_open_details_for_not_user_payout_method(self):
        another_payout_method = PayoutMethodFactory()
        payout_method = PayoutMethodFactory()
        user = payout_method.user
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse('payoutmethod-detail', args=(another_payout_method.id, )))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('payments.stripe_api.create_recipient', lambda *a, **k: stripe_recipient)
    def test_should_create_credit_card(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        url = reverse('payoutmethod-list')
        data = {
            'stripeToken': '123456',
            'name': 'Test Name',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        payout_method = PayoutMethod.objects.filter(user=user).get()
        self.assertEqual(payout_method.stripe_recipient_id, 'recipient_id')

    @patch('payments.stripe_api.create_recipient')
    def test_should_return_stripe_errors(self, create_recipient):
        def raise_stripe_error(*args, **kwargs):
            raise StripeError(message='test error', json_body={
                'error': {
                    'param': 'stripeToken',
                }
            })
        create_recipient.side_effect = raise_stripe_error
        user = UserFactory()
        self.client.force_authenticate(user=user)
        url = reverse('payoutmethod-list')
        data = {
            'stripeToken': '123456',
            'name': 'Test User',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['stripeToken'], 'test error')

        self.assertEqual(PayoutMethod.objects.count(), 0)
