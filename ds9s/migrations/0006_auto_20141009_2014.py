# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0005_auto_20141008_2258'),
    ]

    operations = [
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
        migrations.RenameField(
            model_name='analysis',
            old_name='redshift',
            new_name='value',
        ),
        migrations.RemoveField(
            model_name='analysis',
            name='date_done',
        ),
        migrations.AddField(
            model_name='analysis',
            name='emissionline',
            field=models.ForeignKey(default=1, to='ds9s.EmissionLine'),
            preserve_default=False,
        ),
    ]
