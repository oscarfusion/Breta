# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0010_auto_20150320_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='fee',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
