# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0024_auto_20150228_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milestone',
            name='status',
            field=models.CharField(default=b'NS', max_length=255, choices=[(b'NS', b'No started'), (b'IP', b'In progress'), (b'CM', b'Complete'), (b'ACCEPTED', b'Accepted'), (b'pm-accepted', b'Accepted by PM')]),
            preserve_default=True,
        ),
    ]
