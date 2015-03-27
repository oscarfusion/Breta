# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0032_project_timeline'),
    ]

    operations = [
        migrations.AddField(
            model_name='milestone',
            name='is_due_email_sent',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
