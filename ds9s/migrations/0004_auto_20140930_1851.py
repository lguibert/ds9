# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0003_auto_20140930_1849'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roles',
            old_name='name',
            new_name='NAME_ROLE',
        ),
    ]
