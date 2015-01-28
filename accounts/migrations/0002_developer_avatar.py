# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_squashed_0010_auto_20150126_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='developer',
            name='avatar',
            field=models.FileField(null=True, upload_to=b'avatar_upload_to', blank=True),
            preserve_default=True,
        ),
    ]
