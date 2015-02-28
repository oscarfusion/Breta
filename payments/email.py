from django.conf import settings

from core.email import send_email


def send_payment_confirmation_email(transaction):
    transactions_url = '{}/payments'.format(settings.DOMAIN)
    return send_email([transaction.get_user().email], 'Payment confirmation', 'emails/payments/payment_confirmation.html', {'transaction': transaction, 'transactions_url': transactions_url})
