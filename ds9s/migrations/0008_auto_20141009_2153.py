# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0007_auto_20141009_2152'),
    ]

    operations = [
        migrations.RenameField(
            model_name='galaxy',
            old_name='fields',
            new_name='galaxyfields',
        ),
    ]
