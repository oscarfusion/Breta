# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import breta_messages.models


class Migration(migrations.Migration):

    dependencies = [
        ('breta_messages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagefile',
            name='file',
            field=models.FileField(upload_to=breta_messages.models.file_upload_to),
            preserve_default=True,
        ),
    ]
