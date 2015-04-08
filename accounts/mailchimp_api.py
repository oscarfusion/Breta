import mailchimp

from django.conf import settings


def subscribe_user(user):
    mailchimp_api = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)
    mailchimp_api.lists.subscribe(settings.MAILCHIMP_DEFAULT_LIST, {
        'email': user.email
    }, merge_vars={
        'FNAME': user.first_name,
        'LNAME': user.last_name
    }, double_optin=False, send_welcome=False, update_existing=True)


def subscribe_by_email(email):
    if settings.TESTING:
        return
    mailchimp_api = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)
    mailchimp_api.lists.subscribe(settings.MAILCHIMP_DEFAULT_LIST, {
        'email': email
    }, double_optin=False, send_welcome=False, update_existing=True)


def unsubscribe_user(user):
    mailchimp_api = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)
    mailchimp_api.lists.unsubscribe(settings.MAILCHIMP_DEFAULT_LIST, {
        'email': user.email
    })
