import datetime
from decimal import Decimal
from functools import partial
import pytz

from django.utils import timezone


def transaction_display_at(date):
    tz = pytz.timezone("US/Eastern")
    if timezone.is_aware(date):
        date = tz.normalize(date)
    else:
        date = tz.localize(date)
    day = date.weekday()
    days_offset = 9 - day
    if day == 6 and date.hour >= 9:
        days_offset += 7
    offset = datetime.timedelta(days=days_offset)
    display_at = date + offset
    display_at = display_at.replace(hour=10, minute=0)
    return timezone.get_default_timezone().normalize(display_at)


def filter_transaction(user, transaction):
    from .models import Transaction
    now = timezone.now()
    if user == transaction.payer:
        if transaction.transaction_type == Transaction.ESCROW:
            return True
        elif transaction.transaction_type in [Transaction.PAYOUT, Transaction.PAYPAL_PAYOUT]:
            return transaction.displayed_at <= now
    elif user == transaction.receiver:
        return transaction.displayed_at <= now
    return False


def get_visible_transactions(user, transactions):
    _filter_transaction = partial(filter_transaction, user)
    return filter(_filter_transaction, transactions)


def transaction_amount_for_summ(user_id, now, transaction):
    from .models import Transaction
    if user_id == transaction.payer_id:
        if transaction.transaction_type in [
            Transaction.MILESTONE,
            Transaction.PAYOUT,
            Transaction.PAYPAL_PAYOUT
        ]:
            return -transaction.amount - (transaction.fee or Decimal(0))
    elif user_id == transaction.receiver_id:
        if transaction.transaction_type == Transaction.ESCROW:
            return transaction.amount
        if (
            transaction.transaction_type == Transaction.MILESTONE
            and transaction.displayed_at <= now
        ):
            return transaction.amount
    return Decimal(0)


def get_transactions_summ(user_id, transactions):
    _amount = partial(transaction_amount_for_summ, user_id, timezone.now())
    return sum(map(_amount, transactions))
