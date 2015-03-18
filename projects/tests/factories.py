from django.utils import timezone

import factory
from factory.fuzzy import FuzzyDate, FuzzyDecimal, FuzzyChoice

from ..models import Project, Milestone, Task, ProjectMember


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'projects.Project'

    project_type = FuzzyChoice(choices=Project.PROJECT_CHOICES)
    name = factory.Sequence(lambda n: 'My project %d' % n)
    idea = factory.Sequence(lambda n: 'My idea %d' % n)
    description = factory.Sequence(lambda n: 'My description %d' % n)
    price_range = factory.Sequence(lambda n: '%d,%d' % (n, n+1))
    user = factory.SubFactory('accounts.tests.factories.UserFactory')


class MilestoneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'projects.Milestone'

    status = Milestone.STATUS_IN_PROGRESS
    paid_status = Milestone.PAID_STATUS_DUE
    name = factory.Sequence(lambda n: 'My milestone %d' % n)
    description = factory.Sequence(lambda n: 'My description %d' % n)
    due_date = FuzzyDate(timezone.now().date())
    project = factory.SubFactory('projects.tests.factories.ProjectFactory')
    # amount = FuzzyDecimal(100)


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'projects.Task'

    milestone = factory.SubFactory('projects.tests.factories.MilestoneFactory')
    status = FuzzyChoice(Task.STATUS_CHOICES)
    name = factory.Sequence(lambda n: 'Test name %d' % n)
    description = factory.Sequence(lambda n: 'Test description %d' % n)
    due_date = FuzzyDate(timezone.now().date())
    assigned = factory.SubFactory('accounts.tests.factories.UserFactory')
    amount = FuzzyDecimal(100)


class ProjectMemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'projects.ProjectMember'

    project = factory.SubFactory('projects.tests.factories.ProjectFactory')
    member = factory.SubFactory('accounts.tests.factories.UserFactory')
    status = ProjectMember.STATUS_PENDING
