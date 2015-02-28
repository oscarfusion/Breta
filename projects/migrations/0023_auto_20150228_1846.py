# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0022_project_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='brief',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='brief_ready',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
