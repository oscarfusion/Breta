# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import bitfield.models
import accounts.models
import djorm_pgarray.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [(b'accounts', '0001_initial'), (b'accounts', '0002_auto_20141219_0941'), (b'accounts', '0003_remove_user_region'), (b'accounts', '0004_user_location'), (b'accounts', '0005_developer_portfolioproject_portfolioprojectattachment_website'), (b'accounts', '0006_auto_20150122_1348'), (b'accounts', '0007_developer_project_preferences'), (b'accounts', '0008_auto_20150125_1456'), (b'accounts', '0009_auto_20150125_1500'), (b'accounts', '0010_auto_20150126_1020')]

    dependencies = [
        ('auth', '0001_initial'),
        ('cities_light', '0003_auto_20141120_0342'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(unique=True, max_length=75)),
                ('phone', models.CharField(max_length=255)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to=b'auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to=b'auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
                ('city', models.ForeignKey(blank=True, to='cities_light.City', null=True)),
                ('location', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=1, max_length=255, choices=[(1, b'Developer'), (2, b'Designer')])),
                ('title', models.CharField(max_length=255)),
                ('bio', models.TextField()),
                ('skills', djorm_pgarray.fields.ArrayField(dbtype=b'varchar')),
                ('availability', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PortfolioProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('website', models.CharField(max_length=255)),
                ('image', models.FileField(upload_to=accounts.models.portfolio_project_file_upload_to)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('developer', models.ForeignKey(related_name='portfolio_projects', to='accounts.Developer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PortfolioProjectAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=accounts.models.portfolio_project_file_upload_to)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(related_name='attachments', to='accounts.PortfolioProject')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(default=1, max_length=255, choices=[(1, b'Website'), (2, b'Github')])),
                ('url', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('developer', models.ForeignKey(related_name='websites', to='accounts.Developer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='developer',
            name='availability',
            field=models.CharField(default=b'NOW', max_length=255, choices=[(b'NOW', b'Now')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='developer',
            name='type',
            field=models.CharField(default=b'DEV', max_length=255, choices=[(b'DEV', b'Developer'), (b'DES', b'Designer')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='portfolioproject',
            name='image',
            field=models.FileField(null=True, upload_to=accounts.models.portfolio_project_file_upload_to, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='developer',
            name='project_preferences',
            field=bitfield.models.BitField(((b'lorem', b'Lorem'), (b'sit_amet_consecteur', b'Sit Amet Consecteur'), (b'ipsum_dolor', b'Ipsum Dolor'), (b'adiposcing_elit', b'Adiposcing Elit')), default=None),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='portfolioproject',
            name='skills',
            field=djorm_pgarray.fields.ArrayField(dbtype=b'varchar'),
            preserve_default=True,
        ),
    ]
