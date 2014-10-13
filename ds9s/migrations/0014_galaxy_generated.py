# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0013_auto_20141013_0118'),
    ]

    operations = [
        migrations.AddField(
            model_name='galaxy',
            name='generated',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
