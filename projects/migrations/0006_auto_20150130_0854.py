# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20150129_0937'),
    ]

    operations = [
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('due_date', models.DateField(null=True, blank=True)),
                ('status', models.CharField(default=b'IP', max_length=255, choices=[(b'IP', b'In progress'), (b'CM', b'Complete')])),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('amount', models.DecimalField(max_digits=7, decimal_places=2)),
                ('paid_status', models.CharField(default=b'DUE', max_length=255, choices=[(b'DUE', b'DUE'), (b'PAID', b'PAID')])),
                ('project', models.ForeignKey(related_name='milestones', to='projects.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='projectfile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
