# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import projects.models


class Migration(migrations.Migration):

    replaces = [(b'projects', '0001_initial'), (b'projects', '0002_auto_20141226_1428'), (b'projects', '0003_auto_20141227_1754'), (b'projects', '0004_auto_20141228_1717')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_type', models.CharField(default=b'WS', max_length=255, choices=[(b'WS', b'Website'), (b'TA', b'Tablet app'), (b'PA', b'Phone app'), (b'DP', b'Desktop program')])),
                ('name', models.CharField(max_length=255)),
                ('idea', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price_range', models.CharField(default=b'1-5', max_length=255, choices=[(b'1-5', b'$1000-5000'), (b'5-10', b'$5000-10000')])),
                ('slug', models.SlugField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=projects.models.file_upload_to)),
                ('project', models.ForeignKey(related_name='files', to='projects.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='project',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
    ]
