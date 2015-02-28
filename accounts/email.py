from core.email import send_email


def send_welcome_email(user):
    return send_email([user.email], 'Welcome to breta.com', 'emails/accounts/welcome.html', {'user': user})
