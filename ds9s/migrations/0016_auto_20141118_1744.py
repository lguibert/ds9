# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0015_auto_20141118_1742'),
    ]

    operations = [
        migrations.RenameField(
            model_name='galaxy',
            old_name='last_update',
            new_name='add_date',
        ),
    ]
