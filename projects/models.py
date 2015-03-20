from decimal import Decimal
import os

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q, Sum
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.text import slugify
from constance import config

from accounts.models import User

from . import email


class Project(models.Model):
    WEBSITE = 'WS'
    APP = 'APP'
    WEBSITE_AND_APP = 'WAA'

    PROJECT_CHOICES = (
        (WEBSITE, 'Website'),
        (APP, 'App'),
        (WEBSITE_AND_APP, 'Website & App'),
    )

    BRIEF_NOT_READY = 'not-ready'
    BRIEF_READY = 'ready'
    BRIEF_ACCEPTED = 'accepted'
    BRIEF_DECLINED = 'declined'

    BRIEF_STATUS_CHOICES = (
        (BRIEF_NOT_READY, 'Not ready'),
        (BRIEF_READY, 'Ready'),
        (BRIEF_ACCEPTED, 'Accepted'),
        (BRIEF_DECLINED, 'Declined'),
    )

    project_type = models.CharField(max_length=255, choices=PROJECT_CHOICES, default=WEBSITE)
    name = models.CharField(max_length=255)
    idea = models.CharField(max_length=255)
    description = models.TextField()
    price_range = models.CharField(max_length=255)
    is_sure_about_price = models.BooleanField(default=False)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    members = models.ManyToManyField(User, related_name='projects', through='ProjectMember', through_fields=('project', 'member'), null=True, blank=True)
    manager = models.ForeignKey(User, blank=True, null=True, related_name='manager_projects')
    brief = models.TextField(blank=True, null=True)
    brief_status = models.CharField(max_length=255, choices=BRIEF_STATUS_CHOICES, default=BRIEF_NOT_READY)
    brief_message = models.OneToOneField('ProjectMessage', related_name='project', null=True, blank=True)
    brief_last_edited = models.DateTimeField(default=timezone.now)

    __original_manager = None
    __original_brief_status = None
    __original_brief = None

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)
        self.__original_manager = self.manager
        self.__original_brief_status = self.brief_status
        self.__original_brief = self.brief

    def save(self, *args, **kwargs):
        self.slug = slugify(unicode(self.name))
        if self.__original_manager is None and self.manager is not None:
            from breta_messages.models import Message, MessageRecipient
            email.send_manager_assigned_email(self)
            email.send_project_assigned_email(self)
            msg = Message.objects.create(
                type=Message.TYPE_MESSAGE,
                sender=self.manager,
                subject='New manager %s' % self.name,
                body='I am new manager in %s' % self.name,
                sent_at=timezone.now(),
            )
            msg.save()
            recipient = MessageRecipient(message=msg, recipient=self.user)
            recipient.save()
        if self.__original_brief_status == Project.BRIEF_NOT_READY and self.brief_status == Project.BRIEF_READY:
            email.send_brief_ready_email(self)
        if self.brief != self.__original_brief:
            self.brief_last_edited = timezone.now()
        super(Project, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return '{}/projects/{}'.format(settings.DOMAIN, self.id)

    def get_brief_url(self):
        return '{}/projects/{}/brief'.format(settings.DOMAIN, self.id)

    def get_admin_link(self):
        return '{}{}'.format(settings.API_DOMAIN, reverse('admin:projects_project_change', args=(self.id,)))

    def __unicode__(self):
        return self.name


def project_post_save(sender, instance, created=False, **kwargs):
    if instance.manager is not None and instance.brief_message is None:
        msg = ProjectMessage.objects.create(sender=instance.manager)
        msg.save()
        instance.brief_message = msg
        instance.save()

post_save.connect(project_post_save, sender=Project)


class ProjectMember(models.Model):
    STATUS_PENDING = 'PEN'
    STATUS_REFUSED = 'REF'
    STATUS_ACCEPTED = 'ACC'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_REFUSED, 'Refused'),
        (STATUS_ACCEPTED, 'Accepted'),
    )

    TYPE_OF_WORK_DEVELOPER = 'developer'
    TYPE_OF_WORK_DESIGNER = 'designer'
    TYPE_OF_WORK_CONTENT = 'content'

    TYPE_OF_WORK_CHOICES = (
        (TYPE_OF_WORK_DEVELOPER, 'Developer'),
        (TYPE_OF_WORK_DESIGNER, 'Designer'),
        (TYPE_OF_WORK_CONTENT, 'Content'),
    )

    project = models.ForeignKey(Project, related_name='memberships')
    member = models.ForeignKey(User)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=STATUS_PENDING)
    type_of_work = models.CharField(max_length=255, choices=TYPE_OF_WORK_CHOICES, default=TYPE_OF_WORK_DEVELOPER, null=True, blank=True)
    price_range = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s - %s' % (self.project.name, self.member.get_full_name())


def file_upload_to(instance, filename):
    return 'project_files/%s/%s' % (instance.project.slug, filename)


class ProjectFile(models.Model):
    project = models.ForeignKey(Project, related_name='files')
    file = models.FileField(upload_to=file_upload_to)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    task = models.ForeignKey('Task', related_name='attachments', null=True, blank=True)
    milestone = models.ForeignKey('Milestone', related_name='milestone_attachments', null=True, blank=True)
    author = models.ForeignKey(User, related_name='project_files', null=True, blank=True)
    message = models.ForeignKey('ProjectMessage', related_name='message_attachments', null=True, blank=True)

    def __unicode__(self):
        return '%s - %s' % (self.project.name, self.file)

    @property
    def filename(self):
        return os.path.basename(self.file.name)


class Milestone(models.Model):
    STATUS_NO_STARTED = 'NS'
    STATUS_IN_PROGRESS = 'IP'
    STATUS_COMPLETE = 'CM'
    STATUS_ACCEPTED = 'ACCEPTED'
    STATUS_ACCEPTED_BY_PM = 'pm-accepted'

    STATUS_CHOICES = (
        (STATUS_NO_STARTED, 'No started'),
        (STATUS_IN_PROGRESS, 'In progress'),
        (STATUS_COMPLETE, 'Complete'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_ACCEPTED_BY_PM, 'Accepted by PM'),
    )

    PAID_STATUS_DUE = 'DUE'
    PAID_STATUS_PAID = 'PAID'

    PAID_STATUS_CHOICES = (
        (PAID_STATUS_DUE, 'Due'),
        (PAID_STATUS_PAID, 'Paid'),
    )

    project = models.ForeignKey(Project, related_name='milestones')
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=STATUS_NO_STARTED)
    name = models.CharField(max_length=255)
    description = models.TextField()
    paid_status = models.CharField(max_length=255, choices=PAID_STATUS_CHOICES, default=PAID_STATUS_DUE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    @property
    def amount(self):
        amount = self.tasks.aggregate(Sum('amount')).get('amount__sum') or Decimal(0)
        return amount + amount * Decimal(str(config.PO_FEE / 100.0))

    def try_complete(self, user):
        from activities.models import Activity
        count = self.tasks.count()
        completed_count = self.tasks.filter(status=Task.STATUS_COMPLETE).count()
        if count == completed_count and count != 0:
            self.status = Milestone.STATUS_COMPLETE
            self.save()
            activity = Activity.objects.create(
                milestone=self, project=self.project, type=Activity.TYPE_MILESTONE_STATUS_CHANGED, user=user
            )
            activity.save()
            email.send_milestone_completed_email(self)

    def __unicode__(self):
        return '%s - %s' % (self.project.name if self.project else None, self.name)

    def set_as_paid(self):
        self.paid_status = Milestone.PAID_STATUS_PAID

    def is_paid(self):
        return self.paid_status == Milestone.PAID_STATUS_PAID

    def get_absolute_url(self):
        return '{}/projects/{}/milestones/{}'.format(settings.DOMAIN, self.project_id, self.id)


class Task(models.Model):
    STATUS_DEFAULT = '-'
    STATUS_IN_PROGRESS = 'IP'
    STATUS_COMPLETE = 'CM'
    STATUS_APPROVED = 'APP'

    STATUS_CHOICES = (
        (STATUS_DEFAULT, '-',),
        (STATUS_IN_PROGRESS, 'In progress',),
        (STATUS_COMPLETE, 'Complete',),
        (STATUS_APPROVED, 'Approved',),
    )

    milestone = models.ForeignKey(Milestone, related_name='tasks', blank=True, null=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=STATUS_DEFAULT)
    name = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    assigned = models.ForeignKey(User, related_name='tasks', blank=True, null=True)

    def __unicode__(self):
        return '%s - %s' % (self.milestone.name if self.milestone else None, self.name)

    def get_absolute_url(self):
        return '{}/projects/{}/tasks/{}'.format(settings.DOMAIN, self.milestone.project_id, self.id)


class ProjectMessage(models.Model):
    body = models.CharField(max_length=255, null=True, blank=True)
    sender = models.ForeignKey(User, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    reply_to = models.ForeignKey('self', null=True, blank=True)
    milestone = models.OneToOneField(Milestone, related_name='milestone_message', null=True, blank=True)
    task = models.OneToOneField(Task, related_name='task_message', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __unicode__(self):
        if self.task:
            return '%s - Main' % self.task.name
        elif self.milestone:
            return '%s - Main' % self.milestone.name
        else:
            if not self.body:
                return str(self.pk)
            if len(self.body) > 15:
                return self.body[0:15]
            else:
                return self.body


def task_milestone_post_save(sender, instance, created=False, **kwargs):
    if created:
        if sender is Task:
            message = ProjectMessage(task=instance)
        elif sender is Milestone:
            message = ProjectMessage(milestone=instance)
        else:
            return
        message.save()


post_save.connect(task_milestone_post_save, sender=Task)
post_save.connect(task_milestone_post_save, sender=Milestone)


def project_member_post_save(sender, instance, created=False, **kwargs):
    from breta_messages.models import Message, MessageRecipient
    if created and instance.status == ProjectMember.STATUS_PENDING:
        quote = Quote(project_member=instance, amount=0)
        quote.save()
        msg = Message.objects.create(type=Message.TYPE_QUOTE, project=instance.project, sender=instance.project.manager, quote=quote)
        msg.save()
        recipient = MessageRecipient(message=msg, recipient=instance.member)
        recipient.save()
        email.send_developer_invited_to_project_email(instance, msg)


post_save.connect(project_member_post_save, sender=ProjectMember)


class Quote(models.Model):
    STATUS_PENDING_MEMBER = 'pending-member'
    STATUS_PENDING_OWNER = 'pending-owner'
    STATUS_REFUSED = 'refused'
    STATUS_ACCEPTED = 'accepted'

    STATUS_CHOICES = (
        (STATUS_PENDING_MEMBER, 'Pending member'),
        (STATUS_PENDING_OWNER, 'Pending owner'),
        (STATUS_REFUSED, 'Refused'),
        (STATUS_ACCEPTED, 'Accepted'),
    )

    project_member = models.ForeignKey(ProjectMember, related_name='quotes')
    amount = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=STATUS_PENDING_MEMBER)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __unicode__(self):
        return u'%s - %s' % (self.project_member.project.name if self.project_member and self.project_member.project else None, self.project_member.member.get_full_name() if self.project_member and self.project_member.member else None)

    @classmethod
    def condition_status_project(cls, project):
        return Q(project_member__project=project)

    @classmethod
    def condition_status_developer_type(cls, dev_type):
        return Q(project_member__member__developer__type=dev_type)

    @classmethod
    def condition_status_owner_pending(cls):
        return Q(status=cls.STATUS_PENDING_OWNER)
