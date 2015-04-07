# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0033_milestone_is_due_email_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_demo',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
