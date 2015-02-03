# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20150130_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milestone',
            name='paid_status',
            field=models.CharField(default=b'DUE', max_length=255, choices=[(b'DUE', b'Due'), (b'PAID', b'Paid')]),
            preserve_default=True,
        ),
    ]
