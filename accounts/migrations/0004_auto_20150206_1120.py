# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20150127_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developer',
            name='user',
            field=models.ForeignKey(related_name='developer', to=settings.AUTH_USER_MODEL, unique=True),
            preserve_default=True,
        ),
    ]
