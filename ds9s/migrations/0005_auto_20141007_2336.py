# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0004_auto_20141007_2335'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fits',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('date_upload', models.DateTimeField(auto_now_add=True)),
                ('uniqname', models.CharField(max_length=254, null=True)),
                ('uniq_id', models.IntegerField(default=0)),
                ('generated', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParFileFits',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_par', models.CharField(max_length=254, null=True)),
                ('fieldId_par', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='fits',
            name='parfilefits_id',
            field=models.ForeignKey(to='ds9s.ParFileFits', null=True),
            preserve_default=True,
        ),
    ]
