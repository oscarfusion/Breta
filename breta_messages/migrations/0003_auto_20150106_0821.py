# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('breta_messages', '0002_auto_20141230_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='reply_to',
            field=models.ForeignKey(blank=True, to='breta_messages.Message', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='parent',
            field=models.ForeignKey(related_name='children', blank=True, to='breta_messages.Message', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='messagefile',
            name='message',
            field=models.ForeignKey(related_name='files', to='breta_messages.Message'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='messagerecipient',
            name='message',
            field=models.ForeignKey(related_name='message_recipients', to='breta_messages.Message'),
            preserve_default=True,
        ),
    ]
