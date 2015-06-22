# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def check_user_settings(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    for user in User.objects.all():
        if not isinstance(user.settings, dict):
            user.settings = {}
            user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_auto_20150422_2044'),
    ]

    operations = [
        migrations.RunPython(check_user_settings)
    ]
