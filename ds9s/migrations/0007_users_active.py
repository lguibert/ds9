# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0006_auto_20141001_0330'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
