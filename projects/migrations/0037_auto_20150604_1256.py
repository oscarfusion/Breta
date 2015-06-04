# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0036_auto_20150504_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='idea',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
