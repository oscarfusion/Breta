import factory


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'payments.Customer'

    user = factory.SubFactory('accounts.tests.factories.UserFactory')
    stripe_customer_id = factory.Sequence(lambda n: 'strpie_%d' % n)
    extra_data = {}


class CreditCardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'payments.CreditCard'

    customer = factory.SubFactory(CustomerFactory)
    stripe_card_id = factory.Sequence(lambda n: 'strpie_%d' % n)
    extra_data = {
        'brand': 'VISA',
        'last4': '1234',
        'exp_month': '12',
        'exp_year': '2020',
    }


class PayoutMethodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'payments.PayoutMethod'

    user = factory.SubFactory('accounts.tests.factories.UserFactory')
    stripe_recipient_id = factory.Sequence(lambda n: 'strpie_%d' % n)
    extra_data = {
        'active_account': {
            'bank_name': 'Test bank',
            'routing_number': '100000',
            'last4': '1234',
        }
    }
    name = factory.Sequence(lambda n: 'Name %d' % n)
    address1 = factory.Sequence(lambda n: 'Address %d' % n)
    city = factory.Sequence(lambda n: 'City %d' % n)
    state = factory.Sequence(lambda n: 'State %d' % n)
    zip_code = factory.Sequence(lambda n: 'Zip Code %d' % n)
    country = factory.Sequence(lambda n: 'Country %d' % n)
