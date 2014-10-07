# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0005_auto_20141007_2336'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fits',
            old_name='parfilefits_id',
            new_name='parfilefits',
        ),
    ]
