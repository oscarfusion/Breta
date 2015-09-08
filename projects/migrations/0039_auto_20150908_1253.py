# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0038_auto_20150908_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(default=b'IP', max_length=255, choices=[(b'IP', b'In progress'), (b'CM', b'Complete'), (b'APP', b'Approved')]),
            preserve_default=True,
        ),
    ]
