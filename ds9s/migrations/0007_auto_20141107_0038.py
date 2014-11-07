# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0006_auto_20141107_0019'),
    ]

    operations = [
        migrations.RenameField(
            model_name='identifications',
            old_name='contamined',
            new_name='contaminated',
        ),
    ]
