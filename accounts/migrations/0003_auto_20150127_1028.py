# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_developer_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developer',
            name='avatar',
            field=models.FileField(null=True, upload_to=accounts.models.avatar_upload_to, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='portfolioprojectattachment',
            name='file',
            field=models.FileField(upload_to=accounts.models.portfolio_project_attachment_file_upload_to),
            preserve_default=True,
        ),
    ]
