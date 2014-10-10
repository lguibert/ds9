# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0008_auto_20141009_2153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='galaxy',
            name='galaxyfields',
        ),
        migrations.DeleteModel(
            name='GalaxyFields',
        ),
    ]
