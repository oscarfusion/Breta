from django.conf import settings

from core.email import send_email


def send_new_message_email(user):
    messages_url = '{}/messages/inbox'.format(settings.DOMAIN)
    return send_email([user.email], 'New message', 'emails/messages/new_message.html', {'user': user, 'messages_url': messages_url})
