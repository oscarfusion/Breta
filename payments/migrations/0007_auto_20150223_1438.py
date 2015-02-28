# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_auto_20150220_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='payout_method',
            field=models.ForeignKey(related_name='transactions', blank=True, to='payments.PayoutMethod', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='stripe_id',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(max_length=255, choices=[(b'escrow', b'Payment to Escrow'), (b'milestone', b'Payment to Milestone'), (b'credit', b'Credit'), (b'payout', b'Payout')]),
            preserve_default=True,
        ),
    ]
