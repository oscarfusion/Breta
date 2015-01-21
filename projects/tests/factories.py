import factory

from ..models import Project


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'projects.Project'

    project_type = Project.WEBSITE
    name = factory.Sequence(lambda n: 'My project %d' % n)
    idea = factory.Sequence(lambda n: 'My idea %d' % n)
    description = factory.Sequence(lambda n: 'My description %d' % n)
    price_range = factory.Sequence(lambda n: '%d,%d' % (n, n+1))
    user = factory.SubFactory('accounts.tests.factories.UserFactory')
