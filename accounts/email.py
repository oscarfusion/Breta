from django.conf import settings

from core.email import send_email, send_email_to_admins


def send_welcome_email(user):
    template = 'emails/accounts/welcome_developer.html' if user.developer.first() else 'emails/accounts/welcome.html'
    return send_email([user.email], 'Welcome to breta.com', template, {'user': user})


def send_developer_accepted_email(user):
    login_url = '{}/login'.format(settings.DOMAIN)
    return send_email([user.email], 'You're accepted!', 'emails/accounts/developer_accepted.html', {'user': user, 'login_url': login_url})


def send_password_changed_email(user):
    return send_email([user.email], 'You password on Breta was changed', 'emails/accounts/password_changed.html', {'user': user})


def notify_admins_about_registration(user):
    return send_email_to_admins('%s joined!' % user.get_full_name(), 'emails/accounts/user_joined.html', {'user': user})


def send_invite_email(email, referral_link):
    return send_email([email], 'Thanks, and welcome to Breta :)', 'emails/accounts/invite_user.html', {'referral_link': referral_link})


def send_user_subscribed_email(email):
    return send_email([email], 'Thanks for subscribing to our newsletter!', 'emails/accounts/user_subscribed.html', {})
