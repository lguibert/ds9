# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0006_auto_20141009_2014'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalaxyFields',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('shortname', models.CharField(max_length=254)),
                ('value', models.DecimalField(max_digits=19, decimal_places=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='galaxy',
            name='fields',
            field=models.ForeignKey(default=1, to='ds9s.GalaxyFields'),
            preserve_default=False,
        ),
    ]
