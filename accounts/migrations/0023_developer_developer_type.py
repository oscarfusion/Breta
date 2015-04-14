# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_auto_20150410_0725'),
    ]

    operations = [
        migrations.AddField(
            model_name='developer',
            name='developer_type',
            field=multiselectfield.db.fields.MultiSelectField(default=b'DEV', max_length=7, choices=[(b'DEV', b'Developer'), (b'DES', b'Designer')]),
            preserve_default=True,
        ),
    ]
