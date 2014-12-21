import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'accounts.User'

    first_name = factory.Sequence(lambda n: 'John%d' % n)
    last_name = factory.Sequence(lambda n: 'Galt%d' % n)
    email = factory.Sequence(lambda n: 'johngalt%d@example.com' % n)
    phone = factory.Sequence(lambda n: '123456%d' % n)
    is_active = True
