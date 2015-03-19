# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_auto_20150223_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='displayed_at',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
