# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0010_auto_20150203_0742'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.CharField(max_length=255, null=True, blank=True)),
                ('milestone', models.OneToOneField(related_name='milestone_messages', null=True, blank=True, to='projects.Milestone')),
                ('parent', models.ForeignKey(related_name='children', blank=True, to='projects.ProjectMessage', null=True)),
                ('reply_to', models.ForeignKey(blank=True, to='projects.ProjectMessage', null=True)),
                ('sender', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('task', models.OneToOneField(related_name='task_messages', null=True, blank=True, to='projects.Task')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(related_name='projects', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
