# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0026_auto_20150304_1435'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='milestone',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='milestone',
            name='assigned',
        ),
        migrations.AddField(
            model_name='task',
            name='amount',
            field=models.DecimalField(default=0, max_digits=7, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='assigned',
            field=models.ForeignKey(related_name='tasks', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
