from django.conf import settings

from core.email import send_email


def send_welcome_email(user):
    template = 'emails/accounts/welcome_developer.html' if user.developer.first() else 'emails/accounts/welcome.html'
    return send_email([user.email], 'Welcome to breta.com', template, {'user': user})


def send_developer_accepted_email(user):
    login_url = '{}/login'.format(settings.DOMAIN)
    return send_email([user.email], 'You accepted to beta', 'emails/accounts/developer_accepted.html', {'user': user, 'login_url': login_url})
