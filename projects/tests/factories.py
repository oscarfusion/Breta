from django.utils import timezone

import factory
from factory.fuzzy import FuzzyDate, FuzzyDecimal

from ..models import Project, Milestone


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'projects.Project'

    project_type = Project.WEBSITE
    name = factory.Sequence(lambda n: 'My project %d' % n)
    idea = factory.Sequence(lambda n: 'My idea %d' % n)
    description = factory.Sequence(lambda n: 'My description %d' % n)
    price_range = factory.Sequence(lambda n: '%d,%d' % (n, n+1))
    user = factory.SubFactory('accounts.tests.factories.UserFactory')


class MilestonesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'projects.Milestone'

    status = Milestone.STATUS_IN_PROGRESS
    paid_status = Milestone.PAID_STATUS_DUE
    name = factory.Sequence(lambda n: 'My milestone %d' % n)
    description = factory.Sequence(lambda n: 'My description %d' % n)
    due_date = FuzzyDate(timezone.now().date())
    project = factory.SubFactory('projects.tests.factories.ProjectFactory')
    amount = FuzzyDecimal(100)
