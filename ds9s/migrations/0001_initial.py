# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.DecimalField(max_digits=19, decimal_places=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmissionFeatures',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmissionLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('shortname', models.CharField(max_length=254)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmissionLineFields',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('shortname', models.CharField(max_length=254)),
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
                ('uniq_name', models.CharField(max_length=254, null=True)),
                ('generated', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GalaxyFeatures',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.DecimalField(default=None, max_digits=19, decimal_places=10)),
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
        migrations.CreateModel(
            name='GalaxyType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
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
        migrations.AddField(
            model_name='galaxy',
            name='parfolder',
            field=models.ForeignKey(to='ds9s.ParFolder'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='galaxy',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='ds9s.Analysis'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emissionline',
            name='emissionlinefields',
            field=models.ManyToManyField(to='ds9s.EmissionLineFields', through='ds9s.EmissionFeatures'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emissionline',
            name='galaxys',
            field=models.ManyToManyField(to='ds9s.Galaxy', through='ds9s.Analysis'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emissionfeatures',
            name='emissionline',
            field=models.ForeignKey(to='ds9s.EmissionLine'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emissionfeatures',
            name='emissionlinefields',
            field=models.ForeignKey(to='ds9s.EmissionLineFields'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='analysis',
            name='emissionline',
            field=models.ForeignKey(to='ds9s.EmissionLine'),
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
            name='typegalaxy',
            field=models.ForeignKey(to='ds9s.GalaxyType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='analysis',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
