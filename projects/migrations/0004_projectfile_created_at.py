# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20150127_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectfile',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 28, 14, 5, 59, 915098, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
    ]
