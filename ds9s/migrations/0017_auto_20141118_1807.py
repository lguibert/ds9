# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0016_auto_20141118_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identifications',
            name='redshift',
            field=models.DecimalField(null=True, max_digits=3, decimal_places=2),
        ),
    ]
