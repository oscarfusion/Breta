import stripe

from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_customer(token, email):
    return stripe.Customer.create(
        card=token,
        description=email,
    )


def get_customer(token):
    return stripe.Customer.retrieve(token)


def create_recipient(token, name, email):
    return stripe.Recipient.create(
        name=name,
        type="individual",
        email=email,
        bank_account=token,
    )


def create_transaction(amount, customer_id, card_id, description):
    return stripe.Charge.create(
        amount=amount * 100,
        currency="usd",
        customer=customer_id,
        card=card_id,
        description=description,
    )
