from django.conf import settings

from core.email import send_email


def send_new_message_email(user):
    messages_url = '{}/messages/inbox'.format(settings.DOMAIN)
    return send_email([user.email], 'New message', 'emails/messages/new_message.html', {'user': user, 'messages_url': messages_url})


def send_new_task_comment_email(user, task):
    return send_email([user.email], 'New comment for task {}'.format(task.name), 'emails/messages/new_task_comment.html', {'user': user, 'task': task})


def send_new_milestone_comment_email(user, milestone):
    return send_email([user.email], 'New comment for milestone {}'.format(milestone.name), 'emails/messages/new_milestone_comment.html', {'user': user, 'milestone': milestone})
