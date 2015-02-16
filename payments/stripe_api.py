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
