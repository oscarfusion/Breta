# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('breta_messages', '0005_auto_20150225_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
