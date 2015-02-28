# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0020_auto_20150225_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='status',
            field=models.CharField(default=b'pending-member', max_length=255, choices=[(b'pending-member', b'Pending member'), (b'pending-owner', b'Pending owner'), (b'refused', b'Refused'), (b'accepted', b'Accepted')]),
            preserve_default=True,
        ),
    ]
