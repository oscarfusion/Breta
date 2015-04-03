# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0012_transaction_is_confirm_email_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(max_length=255, choices=[(b'escrow', b'Payment to Escrow'), (b'milestone', b'Payment to Milestone'), (b'credit', b'Credit'), (b'payout', b'Payout'), (b'paypal-payout', b'PayPal payout'), (b'referral-payment', b'Referral payment')]),
            preserve_default=True,
        ),
    ]
