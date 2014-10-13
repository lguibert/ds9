# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0011_galaxyfeatures_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='galaxy',
            name='uniqname',
            field=models.CharField(max_length=254, null=True),
            preserve_default=True,
        ),
    ]
