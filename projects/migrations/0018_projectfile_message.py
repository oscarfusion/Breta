# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_projectfile_milestone'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectfile',
            name='message',
            field=models.ForeignKey(related_name='message_attachments', blank=True, to='projects.ProjectMessage', null=True),
            preserve_default=True,
        ),
    ]
