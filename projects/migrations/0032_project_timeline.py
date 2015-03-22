# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0031_auto_20150320_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='timeline',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
