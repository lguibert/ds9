# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0002_auto_20140930_1803'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roles',
            old_name='NAME_ROLE',
            new_name='name',
        ),
    ]
