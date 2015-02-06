# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_auto_20150204_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmessage',
            name='milestone',
            field=models.OneToOneField(related_name='milestone_message', null=True, blank=True, to='projects.Milestone'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectmessage',
            name='task',
            field=models.OneToOneField(related_name='task_message', null=True, blank=True, to='projects.Task'),
            preserve_default=True,
        ),
    ]
