from django.conf import settings
from django.core.mail import send_mail, mail_admins
from django.template.loader import render_to_string


def send_email(to, subject, template, context):
    context.update({
        'notification_settings_url': '{}/profile/edit/settings'.format(settings.DOMAIN)
    })
    content = render_to_string(template, context)
    return send_mail(
        subject=subject,
        message=content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=to,
        html_message=content,
    )


def send_email_to_admins(subject, template, context):
    context.update({
        'notification_settings_url': '{}/profile/edit/settings'.format(settings.DOMAIN)
    })
    content = render_to_string(template, context)
    return mail_admins(
        message=content,
        html_message=content,
        subject=subject,
    )
