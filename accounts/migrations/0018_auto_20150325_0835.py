# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20150319_0854'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='email',
            options={'verbose_name_plural': 'Newsletter signups'},
        ),
        migrations.AddField(
            model_name='email',
            name='ip_address',
            field=models.GenericIPAddressField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='email',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'Joined date'),
            preserve_default=True,
        ),
    ]
