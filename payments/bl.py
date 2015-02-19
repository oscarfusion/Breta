from decimal import Decimal

from django.db.models import Sum

from .models import Transaction


def get_user_balance(user_id):
    escrow_sum = Transaction.objects.filter(credit_card__customer__user_id=user_id, transaction_type=Transaction.ESCROW).aggregate(Sum('amount')).get('amount__sum') or Decimal(0)
    paid_to_milestones_sum = Transaction.objects.filter(credit_card__customer__user_id=user_id, transaction_type=Transaction.MILESTONE, credit_card__isnull=True).aggregate(Sum('amount')).get('amount__sum') or Decimal(0)
    return str(escrow_sum - paid_to_milestones_sum)
