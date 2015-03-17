# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

from django.db import models, migrations


def fill_referral_codes(apps, schema_editor):
    Email = apps.get_model('accounts', 'Email')
    for email in Email.objects.all():
        email.referral_code = str(uuid.uuid4())
        email.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20150317_0843'),
    ]

    operations = [
        migrations.RunPython(fill_referral_codes)
    ]
