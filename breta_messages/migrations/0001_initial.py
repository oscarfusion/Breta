# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import projects.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('sent_at', models.DateTimeField(null=True, blank=True)),
                ('sender_deleted_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, to='breta_messages.Message', null=True)),
            ],
            options={
                'ordering': ['-sent_at'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MessageFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=projects.models.file_upload_to)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('message', models.ForeignKey(to='breta_messages.Message')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MessageRecipient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('read_at', models.DateTimeField(null=True, blank=True)),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('message', models.ForeignKey(to='breta_messages.Message')),
                ('recipient', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='message',
            name='recipients',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, through='breta_messages.MessageRecipient', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(related_name='sent_messages', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
