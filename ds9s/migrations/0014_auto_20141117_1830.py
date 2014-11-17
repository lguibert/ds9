# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0013_identifications_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identifications',
            name='redshift',
            field=models.DecimalField(null=True, max_digits=19, decimal_places=10),
        ),
    ]
