from django.utils import timezone

from breta.celery import app
from .models import Transaction
from . import email


@app.task()
def transaction_received():
    transactions = Transaction.objects.filter(
        displayed_at__lte=timezone.now(),
        is_confirm_email_sent=False,
        transaction_type__in=[Transaction.MILESTONE, Transaction.PAYOUT]
    )
    for transaction in transactions:
        if transaction.transaction_type == Transaction.MILESTONE:
            email.send_payment_received_email(transaction)
        if transaction.transaction_type == Transaction.PAYOUT:
            email.send_payout_confirmation_email(transaction)
        transaction.is_confirm_email_sent = True
        transaction.save()
