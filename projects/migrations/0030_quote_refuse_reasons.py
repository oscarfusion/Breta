# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import bitfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0029_project_brief_last_edited'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='refuse_reasons',
            field=bitfield.models.BitField(((b'not-available', b"Im' not available"), (b'not-available', b'Budget is unreasonable'), (b'wrong-project-type', b"This isn't the type of project I like")), default=0),
            preserve_default=True,
        ),
    ]
