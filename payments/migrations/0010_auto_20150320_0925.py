# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payments', '0009_auto_20150319_1619'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='user_email',
            new_name='referrer_email',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='user',
        ),
        migrations.AddField(
            model_name='transaction',
            name='fee',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=12, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transaction',
            name='payer',
            field=models.ForeignKey(related_name='payment_transactions', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transaction',
            name='receiver',
            field=models.ForeignKey(related_name='received_transactions', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transaction',
            name='referrer',
            field=models.ForeignKey(related_name='referrals_transactions', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transaction',
            name='referrer_amount',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
