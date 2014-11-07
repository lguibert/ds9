# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0007_auto_20141107_0038'),
    ]

    operations = [
        migrations.AddField(
            model_name='galaxytype',
            name='nameForId',
            field=models.CharField(default=1, max_length=254),
            preserve_default=False,
        ),
    ]
