# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0009_auto_20141107_2004'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalaxyTypes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('nameForId', models.CharField(max_length=254)),
                ('galaxys', models.ManyToManyField(related_name=b'galaxytypes_galaxys_iden', through='ds9s.Identifications', to='ds9s.Galaxy')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='GalaxyType',
        ),
        migrations.AddField(
            model_name='galaxy',
            name='galaxytype',
            field=models.ManyToManyField(to='ds9s.GalaxyTypes', through='ds9s.Identifications'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='identifications',
            name='galaxytype',
            field=models.ForeignKey(default=1, to='ds9s.GalaxyTypes'),
            preserve_default=False,
        ),
    ]
