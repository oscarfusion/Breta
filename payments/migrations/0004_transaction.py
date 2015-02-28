# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgjson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_projectfile_message'),
        ('payments', '0003_auto_20150216_1308'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('stripe_id', models.CharField(max_length=255, null=True)),
                ('extra_data', djorm_pgjson.fields.JSONField(default={}, null=True, blank=True)),
                ('amount', models.DecimalField(max_digits=12, decimal_places=2)),
                ('transaction_type', models.CharField(max_length=255, choices=[(b'escrow', b'Payment to Escrow'), (b'milestone', b'Payment to Milestone'), (b'credit', b'Credit')])),
                ('credit_card', models.ForeignKey(related_name='transactions', to='payments.CreditCard')),
                ('milestone', models.ForeignKey(blank=True, to='projects.Milestone', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
