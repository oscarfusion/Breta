# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0019_quote'),
        ('breta_messages', '0004_auto_20150204_0832'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='project',
            field=models.ForeignKey(related_name='messages', blank=True, to='projects.Project', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='quote',
            field=models.OneToOneField(related_name='message', null=True, blank=True, to='projects.Quote'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='type',
            field=models.CharField(default=b'message', max_length=255, choices=[(b'message', b'Message'), (b'quote', b'Quote')]),
            preserve_default=True,
        ),
    ]
