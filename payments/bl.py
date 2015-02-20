from decimal import Decimal

from django.core.exceptions import PermissionDenied
from django.db.models import Sum

from . import stripe_api
from .models import Transaction, CreditCard


def get_user_balance(user_id):
    escrow_sum = Transaction.objects.filter(credit_card__customer__user_id=user_id, transaction_type=Transaction.ESCROW).aggregate(Sum('amount')).get('amount__sum') or Decimal(0)
    paid_to_milestones_sum = Transaction.objects.filter(credit_card__customer__user_id=user_id, transaction_type=Transaction.MILESTONE, credit_card__isnull=True).aggregate(Sum('amount')).get('amount__sum') or Decimal(0)
    return str(escrow_sum - paid_to_milestones_sum)


def create_transaction(credit_card_id, user, amount=None, transaction_type=Transaction.ESCROW, milestone_id=None):
    stripe_id = None
    extra_data = {}
    if credit_card_id:
        credit_card = CreditCard.objects.get(pk=credit_card_id)
        if credit_card.customer.user != user:
            raise PermissionDenied()
        transaction = stripe_api.create_transaction(Decimal(amount), user.stripe_customer.stripe_customer_id, credit_card.stripe_card_id, user.email)
        stripe_id = transaction.id
        extra_data = transaction.to_dict()
    instance = Transaction.objects.create(
        credit_card_id=credit_card_id,
        stripe_id=stripe_id,
        extra_data=extra_data,
        amount=amount,
        transaction_type=transaction_type,
        milestone_id=milestone_id,
    )
    return instance
