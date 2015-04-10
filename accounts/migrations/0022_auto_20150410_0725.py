# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def fill_user_type_and_complete_signup(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    for user in User.objects.all():
        if user.developer.first():
            user.user_type = 'developer'  # User.DEVELOPER
        else:
            user.user_type = 'project-owner'  # User.PROJECT_OWNER
        user.signup_completed = True
        user.save()


def reverse_migrations(apps, schema_editor):
    return True


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_auto_20150410_0725'),
    ]

    operations = [
        migrations.RunPython(fill_user_type_and_complete_signup, reverse_code=reverse_migrations)
    ]
