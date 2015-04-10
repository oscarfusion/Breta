# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_user_paypal_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='signup_completed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(blank=True, max_length=255, null=True, choices=[(b'project-owner', b'Project Owner'), (b'developer', b'Developer'), (b'other', b'Other')]),
            preserve_default=True,
        ),
    ]
