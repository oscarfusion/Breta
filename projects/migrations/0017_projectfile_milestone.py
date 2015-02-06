# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0016_auto_20150205_1002'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectfile',
            name='milestone',
            field=models.ForeignKey(related_name='milestone_attachments', blank=True, to='projects.Milestone', null=True),
            preserve_default=True,
        ),
    ]
