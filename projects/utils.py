import datetime
from decimal import Decimal
from django.utils.text import slugify
from django.utils.timezone import make_aware, get_current_timezone, now, timedelta
from constance import config


def sort_project_messages(iterable):
    qs = sorted(list(iterable), key=lambda x: x.created_at or make_aware(
        datetime.datetime(datetime.MINYEAR, 1, 1),
        get_current_timezone()
    ))
    res = []
    while qs:
        obj = qs.pop(0)
        res.insert(0, obj)
        pos = res.index(obj) + 1
        replies_to_curr = [y for y in qs if y.reply_to == obj]
        for i, x in enumerate(replies_to_curr):
            res.insert(pos + i, x)
            qs.remove(x)
    return res


def create_demo_project_for_po(user):
    from accounts.models import User
    from .models import Project, Milestone, Task, ProjectMember, ProjectMessage
    try:
        demo_manager = User.objects.get(pk=int(config.DEMO_MANAGER_ID))
        demo_developer = User.objects.get(pk=int(config.DEMO_DEVELOPER_ID))
    except User.DoesNotExist:
        return
    name = u'Your first project'
    project = Project.objects.create(
        project_type=Project.WEBSITE,
        name=name,
        idea='Coolest project ever',
        description="""
        Lorem Ipsum is simply dummy text of the printing and typesetting industry.
        Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
        when an unknown printer took a galley of type and scrambled it to make a type specimen book.
        It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.
        It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
        """,
        price_range='1000,5000',
        slug=slugify(name),
        manager=demo_manager,
        brief="""
        Lorem Ipsum is simply dummy text of the printing and typesetting industry.
        Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
        when an unknown printer took a galley of type and scrambled it to make a type specimen book.
        It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.
        It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
        """,
        brief_status=Project.BRIEF_READY,
        is_demo=True,
        user=user
    )
    brief_msg = ProjectMessage.objects.create(sender=project.manager)
    project.brief_message = brief_msg
    project.save()
    ProjectMember.objects.create(
        project=project,
        member=demo_developer,
        status=ProjectMember.STATUS_ACCEPTED,
        type_of_work=ProjectMember.TYPE_OF_WORK_DEVELOPER,
        price_range='100,750'
    )
    milestone_1 = Milestone.objects.create(
        project=project,
        due_date=now() - timedelta(days=7),
        name='First milestone',
        status=Milestone.STATUS_ACCEPTED,
        description="""
        Lorem Ipsum is simply dummy text of the printing and typesetting industry.
        Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
        """,
        paid_status=Milestone.PAID_STATUS_PAID,
    )
    Task.objects.create(
        milestone=milestone_1,
        status=Task.STATUS_COMPLETE,
        name="First task",
        description="""
        Lorem Ipsum is simply dummy text of the printing and typesetting industry.
        Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
        """,
        due_date=now() - timedelta(days=10),
        amount=Decimal(500),
        assigned=demo_developer
    )
    Task.objects.create(
        milestone=milestone_1,
        status=Task.STATUS_COMPLETE,
        name="Second task",
        description="""
        Lorem Ipsum is simply dummy text of the printing and typesetting industry.
        Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
        """,
        due_date=now() - timedelta(days=8),
        amount=Decimal(300),
        assigned=demo_developer
    )
    milestone_2 = Milestone.objects.create(
        project=project,
        due_date=now() + timedelta(days=10),
        name='Second milestone',
        status=Milestone.STATUS_NO_STARTED,
        description="""
        Lorem Ipsum is simply dummy text of the printing and typesetting industry.
        Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
        """,
        paid_status=Milestone.PAID_STATUS_PAID,
    )
    Task.objects.create(
        milestone=milestone_2,
        status=Task.STATUS_COMPLETE,
        name="Yet another task",
        description="""
        Lorem Ipsum is simply dummy text of the printing and typesetting industry.
        Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
        """,
        due_date=now() + timedelta(days=3),
        amount=Decimal(300),
        assigned=demo_developer
    )
    Task.objects.create(
        milestone=milestone_2,
        status=Task.STATUS_IN_PROGRESS,
        name="Yet another task #2",
        description="""
        Lorem Ipsum is simply dummy text of the printing and typesetting industry.
        Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
        """,
        due_date=now() + timedelta(days=6),
        amount=Decimal(300),
        assigned=demo_developer
    )
    milestone_3 = Milestone.objects.create(
        project=project,
        due_date=now() + timedelta(days=20),
        name='Third milestone',
        status=Milestone.STATUS_IN_PROGRESS,
        description="""
        Lorem Ipsum is simply dummy text of the printing and typesetting industry.
        Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
        """,
        paid_status=Milestone.PAID_STATUS_PAID,
    )
    Task.objects.create(
        milestone=milestone_3,
        status=Task.STATUS_DEFAULT,
        name="Last task",
        description="""
        Lorem Ipsum is simply dummy text of the printing and typesetting industry.
        Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
        """,
        due_date=now() + timedelta(days=15),
        amount=Decimal(300),
        assigned=demo_developer
    )
    return project
