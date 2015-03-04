# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0025_auto_20150302_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectmember',
            name='price_range',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectmember',
            name='type_of_work',
            field=models.CharField(default=b'developer', max_length=255, null=True, blank=True, choices=[(b'developer', b'Developer'), (b'designer', b'Designer'), (b'content', b'Content')]),
            preserve_default=True,
        ),
    ]
