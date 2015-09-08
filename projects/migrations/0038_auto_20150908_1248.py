# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def clear_task_statuses(apps, schema_editor):
    Task = apps.get_model('projects', 'Task')
    Task.objects.filter(status='-').update(status='IP')


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0037_auto_20150604_1256'),
    ]

    operations = [
        migrations.RunPython(clear_task_statuses),
    ]
