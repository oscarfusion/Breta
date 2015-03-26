from django.conf import settings

from core.email import send_email


def send_payment_confirmation_email(transaction):
    transactions_url = '{}/payments'.format(settings.DOMAIN)
    return send_email([transaction.get_user().email], 'Payment confirmation', 'emails/payments/payment_confirmation.html', {'transaction': transaction, 'transactions_url': transactions_url})


def send_new_payment_method_email(payment_method):
    transactions_url = '{}/payments'.format(settings.DOMAIN)
    return send_email([payment_method.customer.user.email], 'New payment method added', 'emails/payments/new_payment_method.html', {'payment_method': payment_method, 'transactions_url': transactions_url})


def send_new_payout_method_email(payout_method):
    transactions_url = '{}/payments'.format(settings.DOMAIN)
    return send_email([payout_method.user.email], 'New payout method added', 'emails/payments/new_payout_method.html', {'payout_method': payout_method, 'transactions_url': transactions_url})
