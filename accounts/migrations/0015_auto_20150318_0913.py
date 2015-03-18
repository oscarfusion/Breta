# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import bitfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20150317_0844'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='from_landing',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='developer',
            name='project_preferences',
            field=bitfield.models.BitField(((b'small', b'Small'), (b'big', b'Big')), default=None),
            preserve_default=True,
        ),
    ]
