import factory
from factory.fuzzy import FuzzyChoice

from ..models import Developer


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'accounts.User'

    first_name = factory.Sequence(lambda n: 'John%d' % n)
    last_name = factory.Sequence(lambda n: 'Galt%d' % n)
    email = factory.Sequence(lambda n: 'johngalt%d@example.com' % n)
    phone = factory.Sequence(lambda n: '123456%d' % n)
    is_active = True


class DeveloperFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'accounts.Developer'

    user = factory.SubFactory('accounts.tests.factories.UserFactory')
    title = factory.Sequence(lambda n: 'Cool developer%d' % n)
    bio = factory.Sequence(lambda n: 'Cool developer%d' % n)
    availability = factory.Sequence(lambda n: 'Available%d' % n)
    type = FuzzyChoice(Developer.TYPE_CHOICES)
