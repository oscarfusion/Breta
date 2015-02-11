# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='type',
            field=models.CharField(max_length=255, choices=[(b'new-task', b'New task created'), (b'new-milestone', b'New milestone created'), (b'task-status-changed', b'Task status changed'), (b'milestone-status-changed', b'Milestone status changed')]),
            preserve_default=True,
        ),
    ]
