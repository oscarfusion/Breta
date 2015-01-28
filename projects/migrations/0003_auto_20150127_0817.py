# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20150121_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_type',
            field=models.CharField(default=b'WS', max_length=255, choices=[(b'WS', b'Website'), (b'APP', b'App'), (b'WAA', b'Website & App')]),
            preserve_default=True,
        ),
    ]
