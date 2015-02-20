from decimal import Decimal
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from mock import patch, Mock

from accounts.tests.factories import UserFactory
from projects.tests.factories import MilestoneFactory
from .factories import CreditCardFactory, CustomerFactory, TransactionFactory
from ..bl import create_transaction
from ..exceptions import PaymentException
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
        milestone = MilestoneFactory(amount=Decimal(100))
        user = milestone.project.user
        customer = CustomerFactory(user=user)
        credit_card = CreditCardFactory(customer=customer)
        transaction = create_transaction(credit_card.id, user, Decimal(100), transaction_type=Transaction.MILESTONE, milestone_id=milestone.id)
        self.assertEqual(transaction.amount, Decimal(100))
        self.assertEqual(transaction.milestone_id, milestone.id)
        self.assertEqual(transaction.transaction_type, Transaction.MILESTONE)
        self.assertEqual(transaction.stripe_id, 'transaction_id')

    def test_create_milestone_from_escrow_hould_not_be_allowed_for_amount_more_than_in_escrow(self):
        user = UserFactory()
        milestone = MilestoneFactory()
        self.assertRaises(PaymentException, create_transaction, None, user, Decimal(100), transaction_type=Transaction.MILESTONE, milestone_id=milestone.id)

    @patch('payments.stripe_api.create_transaction', lambda *a, **k: stripe_transaction)
    def test_for_milestone_should_use_milestone_amount(self):
        milestone = MilestoneFactory(amount=Decimal(1000))
        user = milestone.project.user
        customer = CustomerFactory(user=user)
        credit_card = CreditCardFactory(customer=customer)
        transaction = create_transaction(credit_card.id, user, Decimal(100), transaction_type=Transaction.MILESTONE, milestone_id=milestone.id)
        self.assertEqual(transaction.amount, Decimal(1000))
        self.assertEqual(transaction.milestone_id, milestone.id)
        self.assertEqual(transaction.transaction_type, Transaction.MILESTONE)
        self.assertEqual(transaction.stripe_id, 'transaction_id')

    def test_escrow_without_credit_card_should_not_be_possible(self):
        user = UserFactory()
        self.assertRaises(PaymentException, create_transaction, None, user, Decimal(100), transaction_type=Transaction.ESCROW)

    def test_paying_with_foriegn_credit_card_should_not_be_allowed(self):
        user = UserFactory()
        card = CreditCardFactory()
        self.assertRaises(PermissionDenied, create_transaction, card.id, user, Decimal(100), transaction_type=Transaction.ESCROW)

    @patch('payments.stripe_api.create_transaction', lambda *a, **k: stripe_transaction)
    def test_partial_payment(self):
        milestone = MilestoneFactory(amount=Decimal(100))
        user = milestone.project.user
        customer = CustomerFactory(user=user)
        credit_card = CreditCardFactory(customer=customer)
        TransactionFactory(credit_card=credit_card, transaction_type=Transaction.ESCROW, amount=Decimal(80))
        create_transaction(credit_card.id, user, None, transaction_type=Transaction.MILESTONE, milestone_id=milestone.id)
        self.assertEqual(Transaction.objects.count(), 3)
        Transaction.objects.filter(amount=Decimal(80), transaction_type=Transaction.MILESTONE, credit_card__isnull=True).exists()
        Transaction.objects.filter(amount=Decimal(20), transaction_type=Transaction.MILESTONE, credit_card=credit_card).exists()
