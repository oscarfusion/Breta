from stripe.error import StripeError


class PaymentException(StripeError):
    pass
