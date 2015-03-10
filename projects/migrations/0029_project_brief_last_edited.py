# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0028_project_brief_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='brief_last_edited',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]
