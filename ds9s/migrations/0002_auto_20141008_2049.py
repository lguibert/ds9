# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ds9s', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_done', models.DateTimeField(auto_now_add=True)),
                ('reshift', models.DecimalField(max_digits=19, decimal_places=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Galaxy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uniq_id', models.IntegerField(default=0)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParFolder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_par', models.CharField(max_length=254, null=True)),
                ('fieldId_par', models.IntegerField(default=0)),
                ('date_upload', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='galaxy',
            name='parfolder',
            field=models.ForeignKey(to='ds9s.ParFolder', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='galaxy',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='ds9s.Analysis'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='analysis',
            name='galaxy',
            field=models.ForeignKey(to='ds9s.Galaxy'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='analysis',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
