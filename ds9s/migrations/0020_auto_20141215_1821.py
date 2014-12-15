# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0019_auto_20141210_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='value',
            field=models.DecimalField(max_digits=19, decimal_places=6),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='galaxyfeatures',
            name='value',
            field=models.DecimalField(default=None, max_digits=19, decimal_places=6),
            preserve_default=True,
        ),
    ]
