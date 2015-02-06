from django.db import models

from accounts.models import User
from projects.models import Milestone, Task


class Message(models.Model):
    class Meta:
        ordering = ['-sent_at']

    subject = models.CharField(max_length=255)
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

    def is_system(self):
        return (self.sender is None) and (self.sent_at is not None)

    def __unicode__(self):
        return self.subject


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
