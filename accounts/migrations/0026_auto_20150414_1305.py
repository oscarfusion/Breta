# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_auto_20150410_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developer',
            name='bio',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='developer',
            name='title',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='developer',
            name='type',
            field=multiselectfield.db.fields.MultiSelectField(default=b'DEV', max_length=7, null=True, blank=True, choices=[(b'DEV', b'Developer'), (b'DES', b'Designer')]),
            preserve_default=True,
        ),
    ]
