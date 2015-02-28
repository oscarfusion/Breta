# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_transaction'),
        ('accounts', '0004_auto_20150206_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='developer',
            name='current_payout_method',
            field=models.OneToOneField(related_name='owner', null=True, blank=True, to='payments.PayoutMethod'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='current_credit_card',
            field=models.OneToOneField(related_name='owner', null=True, blank=True, to='payments.CreditCard'),
            preserve_default=True,
        ),
    ]
