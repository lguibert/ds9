# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0012_auto_20141112_2337'),
    ]

    operations = [
        migrations.AddField(
            model_name='identifications',
            name='date',
            field=models.DateTimeField(default=datetime.date(2014, 11, 13), auto_now_add=True),
            preserve_default=False,
        ),
    ]
