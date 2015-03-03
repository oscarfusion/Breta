from django import forms

from ..models import CreditCard, Customer
from .. import stripe_api


class CreateCreditCardForm(forms.Form):
    stripeToken = forms.CharField(required=True)
    isActive = forms.BooleanField(required=False, initial=False)

    def save(self, user):
        try:
            customer_id = user.stripe_customer.stripe_customer_id
            customer = stripe_api.get_customer(customer_id)
            credit_card = customer.cards.create(card=self.cleaned_data['stripeToken'])
            credit_card_obj = CreditCard.objects.create(
                customer=user.stripe_customer,
                stripe_card_id=credit_card.id,
                extra_data=credit_card.to_dict(),
                is_active=self.cleaned_data['isActive']
            )
        except Customer.DoesNotExist:
            customer = stripe_api.create_customer(self.cleaned_data['stripeToken'], user.email)
            customer_obj = Customer.objects.create(
                user=user,
                stripe_customer_id=customer.id,
                extra_data=customer.to_dict(),
            )
            credit_card = customer.cards.data[0]
            credit_card_obj = CreditCard.objects.create(
                customer=customer_obj,
                stripe_card_id=credit_card.id,
                extra_data=customer.cards.data[0].to_dict(),
                is_active=self.cleaned_data['isActive']
            )
        return credit_card_obj
