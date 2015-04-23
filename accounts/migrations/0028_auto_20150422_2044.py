# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.hashers import make_password


def emails_to_users(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    Email = apps.get_model('accounts', 'Email')
    registered_emails = User.objects.values_list('email', flat=True)
    amount = 0
    for email in Email.objects.all():
        if email.email in registered_emails:
            continue
        user = User.objects.create(email=email.email)
        user.password = make_password(None)
        amount += 1
    print 'Moved {} users'.format(amount)


def reverse_migrations(apps, schema_editor):
    return True


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_auto_20150422_1525'),
    ]

    operations = [
        migrations.RunPython(emails_to_users, reverse_code=reverse_migrations)
    ]
