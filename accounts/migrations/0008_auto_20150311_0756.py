# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def move_avatars(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    for user in User.objects.all():
        developer = user.developer.first()
        if developer:
            user.avatar = developer.avatar
            user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_user_avatar'),
    ]

    operations = [
        migrations.RunPython(move_avatars)
    ]
