# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0018_projectfile_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=255, choices=[(b'NT', b'New task created'), (b'NM', b'New milestone created'), (b'TSC', b'Task status changed'), (b'MSC', b'Milestone status changed')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(null=True)),
                ('milestone', models.ForeignKey(blank=True, to='projects.Milestone', null=True)),
                ('project', models.ForeignKey(related_name='project_activities', blank=True, to='projects.Project', null=True)),
                ('task', models.ForeignKey(blank=True, to='projects.Task', null=True)),
                ('user', models.ForeignKey(related_name='activities', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'Activities',
            },
            bases=(models.Model,),
        ),
    ]
