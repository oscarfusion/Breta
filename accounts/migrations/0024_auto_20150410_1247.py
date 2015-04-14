# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def fill_developer_type(apps, schema_editor):
    Developer = apps.get_model('accounts', 'Developer')
    for developer in Developer.objects.all():
        developer.developer_type = developer.type
        developer.save()


def reverse(apps, schema_editor):
    return True


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_developer_developer_type'),
    ]

    operations = [
        migrations.RunPython(fill_developer_type, reverse_code=reverse)
    ]
