# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_auto_20150410_1247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='developer',
            name='developer_type',
        ),
        migrations.AlterField(
            model_name='developer',
            name='type',
            field=multiselectfield.db.fields.MultiSelectField(default=b'DEV', max_length=7, choices=[(b'DEV', b'Developer'), (b'DES', b'Designer')]),
            preserve_default=True,
        ),
    ]
