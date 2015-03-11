# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20150219_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.FileField(null=True, upload_to=accounts.models.avatar_upload_to, blank=True),
            preserve_default=True,
        ),
    ]
