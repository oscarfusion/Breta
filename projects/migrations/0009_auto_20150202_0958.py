# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20150202_0947'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='milestone',
            field=models.ForeignKey(related_name='tasks', blank=True, to='projects.Milestone', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(default=b'-', max_length=255, choices=[(b'-', b'-'), (b'IP', b'In progress'), (b'CM', b'Complete'), (b'APP', b'Approved')]),
            preserve_default=True,
        ),
    ]
