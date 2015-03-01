from core.email import send_email


def send_welcome_email(user):
    template = 'emails/accounts/welcome_developer.html' if user.developer.first() else 'emails/accounts/welcome.html'
    return send_email([user.email], 'Welcome to breta.com', template, {'user': user})
