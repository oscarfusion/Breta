# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_project_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milestone',
            name='status',
            field=models.CharField(default=b'NS', max_length=255, choices=[(b'NS', b'No started'), (b'IP', b'In progress'), (b'CM', b'Complete')]),
            preserve_default=True,
        ),
    ]
