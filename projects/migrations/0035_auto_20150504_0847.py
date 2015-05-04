# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0034_project_is_demo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmember',
            name='member',
            field=models.ForeignKey(related_name='project_memberships', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
