# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0021_auto_20150225_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='manager',
            field=models.ForeignKey(related_name='manager_projects', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
