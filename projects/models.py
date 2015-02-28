import uuid

from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify

from accounts.models import User


class Project(models.Model):
    WEBSITE = 'WS'
    APP = 'APP'
    WEBSITE_AND_APP = 'WAA'

    PROJECT_CHOICES = (
        (WEBSITE, 'Website'),
        (APP, 'App'),
        (WEBSITE_AND_APP, 'Website & App'),
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
    members = models.ManyToManyField(User, related_name='projects', through='ProjectMember',
                                     through_fields=('project', 'member'), null=True, blank=True)

    def files(self):
        return ProjectFile.objects.filter(project=self)

    def save(self, *args, **kwargs):
        self.slug = slugify(unicode(self.name))
        super(Project, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class ProjectMember(models.Model):
    STATUS_PENDING = 'PEN'
    STATUS_REFUSED = 'REF'
    STATUS_ACCEPTED = 'ACC'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_REFUSED, 'Refused'),
        (STATUS_ACCEPTED, 'Accepted'),
    )

    project = models.ForeignKey(Project, related_name='memberships')
    member = models.ForeignKey(User)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s - %s' % (self.project.name, self.member.get_full_name())


def file_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
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


class Milestone(models.Model):
    STATUS_NO_STARTED = 'NS'
    STATUS_IN_PROGRESS = 'IP'
    STATUS_COMPLETE = 'CM'

    STATUS_CHOICES = (
        (STATUS_NO_STARTED, 'No started'),
        (STATUS_IN_PROGRESS, 'In progress'),
        (STATUS_COMPLETE, 'Complete'),
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
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    paid_status = models.CharField(max_length=255, choices=PAID_STATUS_CHOICES, default=PAID_STATUS_DUE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    assigned = models.ForeignKey(User, related_name='milestones', blank=True, null=True)

    def __unicode__(self):
        return '%s - %s' % (self.project.name, self.name)

    def set_as_paid(self):
        self.paid_status = Milestone.PAID_STATUS_PAID

    def is_paid(self):
        return self.paid_status == Milestone.PAID_STATUS_PAID


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

    def __unicode__(self):
        return '%s - %s' % (self.milestone.name, self.name)


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
        msg = Message.objects.create(type=Message.TYPE_QUOTE, project=instance.project, sender=instance.project.user, quote=quote)
        msg.save()
        recipient = MessageRecipient(message=msg, recipient=instance.member)
        recipient.save()


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
        return u'%s - %s' % (self.project_member.project.name, self.project_member.member.get_full_name())
