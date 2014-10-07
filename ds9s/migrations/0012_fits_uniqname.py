# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0011_fits_file_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='fits',
            name='uniqname',
            field=models.CharField(max_length=254, null=True),
            preserve_default=True,
        ),
    ]
