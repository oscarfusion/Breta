from decimal import Decimal

from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from constance import config

from accounts.models import User
from projects.models import Milestone
from . import stripe_api
from . import email
from .exceptions import PaymentException
from .models import Transaction, CreditCard, PayoutMethod


def get_user_balance(user_id):
    escrow_sum = Transaction.objects.filter(receiver__id=user_id).aggregate(Sum('amount')).get('amount__sum') or Decimal(0)
    referral_sum = Transaction.objects.filter(referrer__id=user_id).aggregate(Sum('referrer_amount')).get('referrer_amount__sum') or Decimal(0)
    paid_sum = Transaction.objects.filter(payer__id=user_id).aggregate(Sum('amount')).get('amount__sum') or Decimal(0)
    return escrow_sum + referral_sum - paid_sum


def get_fee_and_referrer_amount(amount):
    total_fee = amount * Decimal(str(config.PO_FEE / 100.0)) + amount * Decimal(str(config.DEVELOPER_FEE))
    referer_amount = amount * Decimal(str(config.REFERRAL_TAX_PERCENT / 100.0))
    final_fee = total_fee - referer_amount
    assert final_fee > 0, (amount, final_fee)
    return final_fee, referer_amount


def create_transaction(credit_card_id, user, amount=None, transaction_type=Transaction.ESCROW, milestone_id=None):
    if transaction_type == Transaction.ESCROW:
        transaction = create_escrow_transaction(credit_card_id, user, amount)
        email.send_payment_confirmation_email(transaction)
    elif transaction_type == Transaction.MILESTONE:
        transaction = create_milestone_transaction(credit_card_id, user, milestone_id)
    elif transaction_type == Transaction.PAYOUT:
        transaction = create_payout_transaction(user, amount)
    else:
        raise NotImplementedError()
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
        receiver=user
    )
    return instance


def create_milestone_transaction(credit_card_id, user, milestone_id):
    milestone = Milestone.objects.get(id=milestone_id)
    if milestone.project.user.id != user.id:
        raise PaymentException('You should not pay for foreign milestone')
    amount = milestone.amount
    user_escrow_amount = get_user_balance(user.id)
    if user_escrow_amount < amount:
        diff = Decimal(amount - user_escrow_amount)
        transaction = create_escrow_transaction(credit_card_id, user, diff)
        email.send_payment_confirmation_email(transaction)
    for task in milestone.tasks.values('assigned').annotate(Sum('amount')):
        try:
            receiver = User.objects.get(pk=task.get('assigned'))
        except User.DoesNotExist:
            receiver
        task_amount = task.get('amount__sum', Decimal(0))
        if user.referrer:
            fee, referrer_amount = get_fee_and_referrer_amount(task_amount)
        else:
            fee = task_amount * Decimal(str(config.PO_FEE / 100.0)) + task_amount * Decimal(str(config.DEVELOPER_FEE / 100.0))
            referrer_amount = 0
        task_amount -= task_amount * Decimal(str(config.DEVELOPER_FEE / 100.0))
        transaction = Transaction.objects.create(
            transaction_type=Transaction.MILESTONE,
            amount=task_amount,
            credit_card_id=None,
            payer=user,
            receiver=receiver,
            fee=fee,
            referrer_amount=referrer_amount,
            referrer=user.referrer,
            referrer_email=user.referrer_email,
            milestone_id=milestone_id
        )
        email.send_payment_confirmation_email(transaction)
    milestone.set_as_paid()
    milestone.save()
    return None


def create_payout_transaction(user, amount):
    payout_method = PayoutMethod.objects.filter(user=user, is_active=True).first()
    user_escrow_amount = get_user_balance(user.id)
    if payout_method and user_escrow_amount >= amount:
        transfer = stripe_api.create_transfer(amount, payout_method.stripe_recipient_id, 'Withdraw transfer')
        Transaction.objects.create(
            payout_method=payout_method,
            stripe_id=transfer.id,
            extra_data=transfer.to_dict(),
            amount=amount,
            transaction_type=Transaction.PAYOUT,
            receiver=user
        )
