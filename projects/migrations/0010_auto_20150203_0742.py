# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0009_auto_20150202_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectfile',
            name='author',
            field=models.ForeignKey(related_name='project_files', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectfile',
            name='task',
            field=models.ForeignKey(related_name='attachments', blank=True, to='projects.Task', null=True),
            preserve_default=True,
        ),
    ]
