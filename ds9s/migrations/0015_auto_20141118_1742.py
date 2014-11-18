# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0014_auto_20141117_1830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='identifications',
            name='date',
        ),
        migrations.AddField(
            model_name='identifications',
            name='last_update',
            field=models.DateTimeField(default=datetime.date(2014, 11, 18), auto_now=True),
            preserve_default=False,
        ),
    ]
