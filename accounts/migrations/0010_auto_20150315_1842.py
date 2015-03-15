# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import accounts.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_developer_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='referral_code',
            field=models.CharField(default=accounts.models.get_referral_code, max_length=255),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='referrer',
            field=models.ForeignKey(related_name='invited_users', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
