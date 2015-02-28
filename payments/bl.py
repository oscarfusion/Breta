from decimal import Decimal

from django.core.exceptions import PermissionDenied
from django.db.models import Sum

from projects.models import Milestone
from . import stripe_api
from . import email
from .exceptions import PaymentException
from .models import Transaction, CreditCard, PayoutMethod


def get_user_balance(user_id):
    escrow_sum = Transaction.objects.filter(credit_card__customer__user_id=user_id, transaction_type=Transaction.ESCROW).aggregate(Sum('amount')).get('amount__sum') or Decimal(0)
    paid_to_milestones_sum = Transaction.objects.filter(credit_card__customer__user_id=user_id, transaction_type=Transaction.MILESTONE, credit_card__isnull=True).aggregate(Sum('amount')).get('amount__sum') or Decimal(0)
    return escrow_sum - paid_to_milestones_sum


def create_transaction(credit_card_id, user, amount=None, transaction_type=Transaction.ESCROW, milestone_id=None):
    if transaction_type == Transaction.ESCROW:
        transaction = create_escrow_transaction(credit_card_id, user, amount)
    elif transaction_type == Transaction.MILESTONE:
        transaction = create_milestone_transaction(credit_card_id, user, milestone_id)
    else:
        raise NotImplementedError()
    email.send_payment_confirmation_email(transaction)
    return transaction


def create_escrow_transaction(credit_card_id, user, amount):
    if credit_card_id is None:
        raise PaymentException('Escrow without providing credit card not possible')
    credit_card = CreditCard.objects.get(pk=credit_card_id)
    if credit_card.customer.user != user:
        raise PermissionDenied()
    transaction = stripe_api.create_transaction(Decimal(amount), user.stripe_customer.stripe_customer_id, credit_card.stripe_card_id, user.email)
    instance = Transaction.objects.create(
        credit_card_id=credit_card_id,
        stripe_id=transaction.id,
        extra_data=transaction.to_dict(),
        amount=amount,
        transaction_type=Transaction.ESCROW,
        milestone_id=None,
    )
    return instance


def create_milestone_transaction(credit_card_id, user, milestone_id):
    milestone = Milestone.objects.get(id=milestone_id)
    if milestone.project.user.id != user.id:
        raise PaymentException('You should not pay for foreign milestone')
    amount = milestone.amount
    user_escrow_amount = get_user_balance(user.id)
    if user_escrow_amount > 0:
        amount_from_escrow = amount if user_escrow_amount >= amount else user_escrow_amount
        instance = Transaction.objects.create(
            credit_card_id=None,
            stripe_id=None,
            amount=amount_from_escrow,
            transaction_type=Transaction.MILESTONE,
            milestone=milestone,
        )
        amount = amount - amount_from_escrow
    if amount > 0:
        credit_card = CreditCard.objects.get(pk=credit_card_id)
        if credit_card.customer.user != user:
            raise PermissionDenied()
        transaction = stripe_api.create_transaction(Decimal(amount), user.stripe_customer.stripe_customer_id, credit_card.stripe_card_id, user.email)
        instance = Transaction.objects.create(
            credit_card_id=credit_card_id,
            stripe_id=transaction.id,
            extra_data=transaction.to_dict(),
            amount=amount,
            transaction_type=Transaction.MILESTONE,
            milestone=milestone,
        )
    milestone.set_as_paid()
    milestone.save()
    return instance


def create_milestone_transfer(milestone):
    amount = milestone.amount
    payout_method = PayoutMethod.objects.filter(user=milestone.assigned, is_active=True).first()
    if payout_method:
        transfer = stripe_api.create_transfer(amount, payout_method.stripe_recipient_id, 'Transfer for milestone {}'.format(milestone.id))
        Transaction.objects.create(
            payout_method=payout_method,
            stripe_id=transfer.id,
            extra_data=transfer.to_dict(),
            amount=amount,
            transaction_type=Transaction.PAYOUT,
            milestone=milestone
        )
