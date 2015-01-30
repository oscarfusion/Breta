# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_projectfile_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectfile',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 29, 9, 37, 7, 919867, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
    ]
