from functools import partial
import datetime
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
    now = timezone.now()
    if user == transaction.payer:
        return True
    elif user == transaction.receiver:
        return transaction.displayed_at <= now
    return False


def get_visible_transactions(user, transactions):
    _filter_transaction = partial(filter_transaction, user)
    return filter(_filter_transaction, transactions)
