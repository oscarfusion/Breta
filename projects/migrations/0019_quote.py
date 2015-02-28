# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_projectfile_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True)),
                ('status', models.CharField(default=b'pending', max_length=255, choices=[(b'pending', b'Pending'), (b'refused', b'Refused'), (b'accepted', b'Accepted')])),
                ('project_member', models.ForeignKey(related_name='quotes', to='projects.ProjectMember')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
