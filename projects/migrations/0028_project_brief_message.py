# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0027_auto_20150308_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='brief_message',
            field=models.OneToOneField(related_name='project', null=True, blank=True, to='projects.ProjectMessage'),
            preserve_default=True,
        ),
    ]
