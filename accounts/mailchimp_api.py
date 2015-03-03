import mailchimp

from django.conf import settings


def subscribe_user(user):
    mailchimp_api = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)
    mailchimp_api.lists.subscribe(settings.MAILCHIMP_DEFAULT_LIST, {
        'email': user.email
    }, merge_vars={
        'FNAME': user.first_name,
        'LNAME': user.last_name
    }, update_existing=True)
