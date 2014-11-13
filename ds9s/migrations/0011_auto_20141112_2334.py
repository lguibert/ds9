# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0010_auto_20141107_2004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emissionline',
            name='galaxys',
        ),
        migrations.AddField(
            model_name='analysis',
            name='emissionlinefield',
            field=models.ForeignKey(default=1, to='ds9s.EmissionLineFields'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='emissionline',
            name='emissionlinefields',
            field=models.ManyToManyField(to=b'ds9s.EmissionLineFields', through='ds9s.Analysis'),
        ),
    ]
