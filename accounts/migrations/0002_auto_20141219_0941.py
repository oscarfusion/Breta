# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0003_auto_20141120_0342'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.ForeignKey(blank=True, to='cities_light.City', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='region',
            field=models.ForeignKey(blank=True, to='cities_light.Region', null=True),
            preserve_default=True,
        ),
    ]
