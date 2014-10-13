# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0012_galaxy_uniqname'),
    ]

    operations = [
        migrations.RenameField(
            model_name='galaxy',
            old_name='uniqname',
            new_name='uniq_name',
        ),
    ]
