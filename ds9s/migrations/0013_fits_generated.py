# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0012_fits_uniqname'),
    ]

    operations = [
        migrations.AddField(
            model_name='fits',
            name='generated',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
