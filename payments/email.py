from django.conf import settings

from core.email import send_email, send_email_to_admins


def send_payment_confirmation_email(transaction):
    if transaction.get_user().safe_settings.get('payment_confirmation_email', True):
        transactions_url = '{}/payments'.format(settings.DOMAIN)
        return send_email([transaction.get_user().email], 'Payment confirmation', 'emails/payments/payment_confirmation.html', {'transaction': transaction, 'transactions_url': transactions_url})


def send_new_payment_method_email(payment_method):
    if payment_method.customer.user.safe_settings.get('new_payment_method', True):
        transactions_url = '{}/payments'.format(settings.DOMAIN)
        return send_email([payment_method.customer.user.email], 'New payment method added', 'emails/payments/new_payment_method.html', {'payment_method': payment_method, 'transactions_url': transactions_url})


def send_new_payout_method_email(payout_method):
    if payout_method.user.safe_settings.get('new_payout_method', True):
        transactions_url = '{}/payments'.format(settings.DOMAIN)
        return send_email([payout_method.user.email], 'New payout method added', 'emails/payments/new_payout_method.html', {'payout_method': payout_method, 'transactions_url': transactions_url})


def send_payment_received_email(transaction):
    if transaction.receiver.safe_settings.get('payment_received_email', True):
        transactions_url = '{}/payments'.format(settings.DOMAIN)
        return send_email([transaction.receiver.email], 'New payment received', 'emails/payments/payment_received.html', {'transaction': transaction, 'transactions_url': transactions_url})


def send_payout_confirmation_email(transaction):
    if transaction.receiver.safe_settings.get('payout_confirmation_email', True):
        transactions_url = '{}/payments'.format(settings.DOMAIN)
        return send_email([transaction.receiver.email], 'Payout confirmation', 'emails/payments/payout_confirmation.html', {'transaction': transaction, 'transactions_url': transactions_url})


def send_paypal_payout_request_to_admins(user, amount):
    context = {
        'user': user,
        'amount': amount
    }
    return send_email_to_admins('New PayPal-withdraw request', 'emails/payments/paypal_request.html', context)
