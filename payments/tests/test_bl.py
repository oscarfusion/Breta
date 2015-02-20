from decimal import Decimal
from django.test import TestCase
from mock import patch, Mock

from accounts.tests.factories import UserFactory
from projects.tests.factories import MilestoneFactory
from .factories import CreditCardFactory
from ..bl import create_transaction
from ..models import Transaction


stripe_transaction = Mock(
    id='transaction_id',
    to_dict=lambda: {},
)


class CreateTransactionTestCase(TestCase):
    @patch('payments.stripe_api.create_transaction', lambda *a, **k: stripe_transaction)
    def test_create_escrow(self):
        credit_card = CreditCardFactory()
        user = credit_card.customer.user
        transaction = create_transaction(credit_card.id, user, Decimal(100), transaction_type=Transaction.ESCROW)
        self.assertEqual(transaction.amount, Decimal(100))
        self.assertIsNone(transaction.milestone)
        self.assertEqual(transaction.transaction_type, Transaction.ESCROW)
        self.assertEqual(transaction.stripe_id, 'transaction_id')

    @patch('payments.stripe_api.create_transaction', lambda *a, **k: stripe_transaction)
    def test_create_milestone(self):
        credit_card = CreditCardFactory()
        milestone = MilestoneFactory()
        user = credit_card.customer.user
        transaction = create_transaction(credit_card.id, user, Decimal(100), transaction_type=Transaction.MILESTONE, milestone_id=milestone.id)
        self.assertEqual(transaction.amount, Decimal(100))
        self.assertEqual(transaction.milestone_id, milestone.id)
        self.assertEqual(transaction.transaction_type, Transaction.MILESTONE)
        self.assertEqual(transaction.stripe_id, 'transaction_id')

    def test_create_milestone_from_escrow_money(self):
        user = UserFactory()
        milestone = MilestoneFactory()
        transaction = create_transaction(None, user, Decimal(100), transaction_type=Transaction.MILESTONE, milestone_id=milestone.id)
        self.assertEqual(transaction.amount, Decimal(100))
        self.assertEqual(transaction.milestone_id, milestone.id)
        self.assertEqual(transaction.transaction_type, Transaction.MILESTONE)
        self.assertIsNone(transaction.stripe_id)
        self.assertIsNone(transaction.credit_card)
