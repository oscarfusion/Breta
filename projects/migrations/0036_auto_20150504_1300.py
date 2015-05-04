# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0035_auto_20150504_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='user',
            field=models.ForeignKey(related_name='own_projects', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
