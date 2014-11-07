# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0008_galaxytype_nameforid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='galaxy',
            name='galaxytype',
        ),
        migrations.RemoveField(
            model_name='galaxytype',
            name='galaxys',
        ),
        migrations.RemoveField(
            model_name='identifications',
            name='galaxytype',
        ),
    ]
