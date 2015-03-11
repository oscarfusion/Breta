# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20150311_0756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='developer',
            name='avatar',
        ),
    ]
