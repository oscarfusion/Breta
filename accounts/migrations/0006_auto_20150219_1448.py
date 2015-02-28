# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20150219_0729'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='developer',
            name='current_payout_method',
        ),
        migrations.RemoveField(
            model_name='user',
            name='current_credit_card',
        ),
    ]
