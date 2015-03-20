from decimal import Decimal
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from constance import config
from mock import patch, Mock

from accounts.tests.factories import UserFactory
from projects.tests.factories import MilestoneFactory, TaskFactory
from .factories import CreditCardFactory, CustomerFactory
from ..bl import create_transaction, get_user_balance, get_fee_and_referrer_amount
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
        milestone = MilestoneFactory()
        milestone.save()
        task = TaskFactory(milestone=milestone, amount=Decimal(100))
        task.save()
        user = milestone.project.user
        customer = CustomerFactory(user=user)
        credit_card = CreditCardFactory(customer=customer)
        create_transaction(credit_card.id, user, Decimal(300), transaction_type=Transaction.ESCROW, milestone_id=None)
        total_amount = Decimal(100)
        create_transaction(credit_card.id, user, total_amount, transaction_type=Transaction.MILESTONE, milestone_id=milestone.id)
        final_amount = total_amount - Decimal(str(total_amount * 1 / config.BRETA_FEE))
        transaction = Transaction.objects.filter(milestone__id=milestone.id).first()
        self.assertEqual(transaction.amount, final_amount)
        self.assertEqual(transaction.milestone_id, milestone.id)
        self.assertEqual(transaction.transaction_type, Transaction.MILESTONE)

    def test_create_milestone_from_escrow_hould_not_be_allowed_for_amount_more_than_in_escrow(self):
        user = UserFactory()
        milestone = MilestoneFactory()
        self.assertRaises(PaymentException, create_transaction, None, user, Decimal(100), transaction_type=Transaction.MILESTONE, milestone_id=milestone.id)

    @patch('payments.stripe_api.create_transaction', lambda *a, **k: stripe_transaction)
    def test_for_milestone_should_use_milestone_amount(self):
        milestone = MilestoneFactory()
        milestone.save()
        task = TaskFactory(milestone=milestone, amount=Decimal(1000))
        task.save()
        user = milestone.project.user
        customer = CustomerFactory(user=user)
        credit_card = CreditCardFactory(customer=customer)
        total_amount = Decimal(1000)
        final_amount = total_amount - Decimal(str(total_amount * 1 / config.BRETA_FEE))
        create_transaction(credit_card.id, user, Decimal(1500), transaction_type=Transaction.ESCROW, milestone_id=None)
        create_transaction(credit_card.id, user, Decimal(1000), transaction_type=Transaction.MILESTONE, milestone_id=milestone.id)
        transaction = Transaction.objects.filter(milestone__id=milestone.id).first()
        self.assertEqual(transaction.amount, final_amount)
        self.assertEqual(transaction.milestone_id, milestone.id)
        self.assertEqual(transaction.transaction_type, Transaction.MILESTONE)

    @patch('payments.stripe_api.create_transaction', lambda *a, **k: stripe_transaction)
    def test_payout_transaction(self):
        milestone = MilestoneFactory()
        milestone.save()
        assigned = UserFactory()
        task = TaskFactory(milestone=milestone, amount=Decimal(1000), assigned=assigned)
        task.save()
        user = milestone.project.user
        customer = CustomerFactory(user=user)
        credit_card = CreditCardFactory(customer=customer)
        create_transaction(credit_card.id, user, Decimal(1500), transaction_type=Transaction.ESCROW, milestone_id=None)
        assigned_balance = get_user_balance(assigned.id)
        self.assertEqual(assigned_balance, 0)
        create_transaction(credit_card.id, user, Decimal(1000), transaction_type=Transaction.MILESTONE, milestone_id=milestone.id)
        expected_amount = task.amount - Decimal(str(task.amount * config.BRETA_FEE / 100))
        assigned_balance = get_user_balance(assigned.id)
        self.assertEqual(assigned_balance, expected_amount)

    def test_escrow_without_credit_card_should_not_be_possible(self):
        user = UserFactory()
        self.assertRaises(PaymentException, create_transaction, None, user, Decimal(100), transaction_type=Transaction.ESCROW)

    def test_paying_with_foriegn_credit_card_should_not_be_allowed(self):
        user = UserFactory()
        card = CreditCardFactory()
        self.assertRaises(PermissionDenied, create_transaction, card.id, user, Decimal(100), transaction_type=Transaction.ESCROW)


class TestEscrowAmount(TestCase):
    @patch('payments.stripe_api.create_transaction', lambda *a, **k: stripe_transaction)
    def test_escrow_amount_equals_zero(self):
        user = UserFactory()
        amount = get_user_balance(user.id)
        self.assertEqual(amount, Decimal(0))

    @patch('payments.stripe_api.create_transaction', lambda *a, **k: stripe_transaction)
    def test_escrow_amount_equals_number(self):
        user = UserFactory()
        customer = CustomerFactory(user=user)
        credit_card = CreditCardFactory(customer=customer)
        total_amount = Decimal(1000)
        create_transaction(credit_card.id, user, total_amount, transaction_type=Transaction.ESCROW, milestone_id=None)
        amount = get_user_balance(user.id)
        self.assertEqual(amount, total_amount)

    @patch('payments.stripe_api.create_transaction', lambda *a, **k: stripe_transaction)
    def test_two_escrow_payments(self):
        user = UserFactory()
        customer = CustomerFactory(user=user)
        credit_card = CreditCardFactory(customer=customer)
        total_amount_1 = Decimal(1000)
        total_amount_2 = Decimal(2000)
        create_transaction(credit_card.id, user, total_amount_1, transaction_type=Transaction.ESCROW, milestone_id=None)
        create_transaction(credit_card.id, user, total_amount_2, transaction_type=Transaction.ESCROW, milestone_id=None)
        amount = get_user_balance(user.id)
        self.assertEqual(amount, total_amount_1 + total_amount_2)


class TestCalculatingFeeAndReferralAmount(TestCase):
    def test_raises_assertion_error(self):
        amount = Decimal(0.0)
        self.assertRaises(AssertionError, get_fee_and_referrer_amount, amount)

    def test_expected_results(self):
        amount = Decimal(100)
        expected_total_fee = amount * Decimal(str(config.PO_FEE / 100.0)) + amount * Decimal(str(config.DEVELOPER_FEE))
        expected_referrer_amount = amount * Decimal(str(config.REFERRAL_TAX_PERCENT / 100.0))
        expected_final_fee = expected_total_fee - expected_referrer_amount
        fee, referral_amount = get_fee_and_referrer_amount(amount)
        self.assertEqual(expected_final_fee, fee)
        self.assertEqual(expected_referrer_amount, referral_amount)
