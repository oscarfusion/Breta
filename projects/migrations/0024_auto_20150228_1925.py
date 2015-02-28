# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0023_auto_20150228_1846'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='brief_ready',
        ),
        migrations.AddField(
            model_name='project',
            name='brief_status',
            field=models.CharField(default=b'not-ready', max_length=255, choices=[(b'not-ready', b'Not ready'), (b'ready', b'Ready'), (b'accepted', b'Accepted'), (b'declined', b'Declined')]),
            preserve_default=True,
        ),
    ]
