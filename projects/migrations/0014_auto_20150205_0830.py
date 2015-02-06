# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0013_projectmessage_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'PEN', max_length=255, choices=[(b'PEN', b'Pending'), (b'REF', b'Refused'), (b'ACC', b'Accepted')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('member', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(related_name='memberships', to='projects.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='project',
            name='members',
        ),
    ]
