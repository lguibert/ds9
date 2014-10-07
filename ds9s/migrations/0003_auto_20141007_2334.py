# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0002_auto_20141007_2332'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fits',
            old_name='parfiefits_id',
            new_name='parfilefits_id',
        ),
    ]
