from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

from accounts.models import User
from projects.models import Milestone, Task

from . import bl
from . import email


class Message(models.Model):
    class Meta:
        ordering = ['-sent_at']

    TYPE_MESSAGE = 'message'
    TYPE_QUOTE = 'quote'

    TYPE_CHOICES = (
        (TYPE_MESSAGE, 'Message'),
        (TYPE_QUOTE, 'Quote'),
    )

    type = models.CharField(max_length=255, choices=TYPE_CHOICES, default=TYPE_MESSAGE)
    subject = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField()
    sender = models.ForeignKey(User, related_name='sent_messages', null=True)
    recipients = models.ManyToManyField(User, through='MessageRecipient',
                                        through_fields=('message', 'recipient',), null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    reply_to = models.ForeignKey('self', null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    sender_deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    milestone = models.OneToOneField(Milestone, related_name='message', null=True, blank=True)
    task = models.OneToOneField(Task, related_name='message', null=True, blank=True)
    project = models.ForeignKey('projects.Project', related_name='messages', null=True, blank=True)
    quote = models.OneToOneField('projects.Quote', related_name='message', null=True, blank=True)

    def is_system(self):
        return (self.sender is None) and (self.sent_at is not None)

    def get_absolute_url(self):
        return '{}/messages/inbox/{}'.format(settings.DOMAIN, self.id)

    def get_quote_url(self):
        return '{}/messages/quote-requests/{}'.format(settings.DOMAIN, self.id)

    # def __unicode__(self):
    #     return self.subject


class MessageRecipient(models.Model):
    recipient = models.ForeignKey(User)
    message = models.ForeignKey(Message, related_name='message_recipients')
    read_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def file_upload_to(instance, filename):
    return 'message_files/%s/%s' % (instance.message.id, filename)


class MessageFile(models.Model):
    message = models.ForeignKey(Message, related_name='files')
    file = models.FileField(upload_to=file_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)


def message_recipient_save(sender, instance, created=False, **kwargs):
    if created:
        not_read_count = MessageRecipient.objects.filter(recipient=instance.recipient, read_at__isnull=True).count()
        if not_read_count == 1:
            email.send_new_message_email(instance.recipient)


def message_save(sender, instance, created=False, **kwargs):
    if created:
        if instance.task is not None:
            bl.notify_about_new_task_comment(instance)
        elif instance.milestone is not None:
            bl.notify_about_new_milestone_comment(instance)


post_save.connect(message_recipient_save, sender=MessageRecipient)
post_save.connect(message_save, sender=Message)
