# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0003_auto_20141007_2334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fits',
            name='parfilefits_id',
        ),
        migrations.DeleteModel(
            name='Fits',
        ),
        migrations.DeleteModel(
            name='ParFileFits',
        ),
    ]
