# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20141219_0941'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='region',
        ),
    ]
