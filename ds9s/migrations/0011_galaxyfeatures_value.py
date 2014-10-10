# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0010_auto_20141009_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='galaxyfeatures',
            name='value',
            field=models.DecimalField(default=None, max_digits=19, decimal_places=10),
            preserve_default=True,
        ),
    ]
