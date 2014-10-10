# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0009_auto_20141009_2202'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalaxyFeatures',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('galaxy', models.ForeignKey(to='ds9s.Galaxy')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GalaxyFields',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('shortname', models.CharField(max_length=254)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='galaxyfeatures',
            name='galaxyfields',
            field=models.ForeignKey(to='ds9s.GalaxyFields'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='galaxy',
            name='galaxyfields',
            field=models.ManyToManyField(to='ds9s.GalaxyFields', through='ds9s.GalaxyFeatures'),
            preserve_default=True,
        ),
    ]
