# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0011_auto_20150320_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='is_confirm_email_sent',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
