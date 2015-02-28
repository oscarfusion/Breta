# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_auto_20150219_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='credit_card',
            field=models.ForeignKey(related_name='transactions', blank=True, to='payments.CreditCard', null=True),
            preserve_default=True,
        ),
    ]
