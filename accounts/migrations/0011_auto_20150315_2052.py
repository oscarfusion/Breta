# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

from django.db import models, migrations


def fill_referral_codes(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    for user in User.objects.all():
        user.referral_code = str(uuid.uuid4())
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20150315_1842'),
    ]

    operations = [
        migrations.RunPython(fill_referral_codes)
    ]
