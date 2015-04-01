# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_auto_20150302_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='type',
            field=models.CharField(max_length=255, choices=[(b'new-project', b'New project created'), (b'new-task', b'New task created'), (b'new-milestone', b'New milestone created'), (b'task-status-changed', b'Task status changed'), (b'milestone-status-changed', b'Milestone status changed'), (b'project-completed', b'Project completed'), (b'milestone-accepted', b'Milestone accepted'), (b'milestone-accepted-by-pm', b'Milestone accepted by PM')]),
            preserve_default=True,
        ),
    ]
