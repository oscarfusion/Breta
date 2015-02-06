# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_auto_20150203_0742'),
        ('breta_messages', '0003_auto_20150106_0821'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='milestone',
            field=models.OneToOneField(related_name='message', null=True, blank=True, to='projects.Milestone'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='task',
            field=models.OneToOneField(related_name='message', null=True, blank=True, to='projects.Task'),
            preserve_default=True,
        ),
    ]
