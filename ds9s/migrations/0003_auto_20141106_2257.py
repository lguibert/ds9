# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0002_auto_20141106_2256'),
    ]

    operations = [
        migrations.RenameField(
            model_name='analysis',
            old_name='typeeeegalaxy',
            new_name='typegalaxy',
        ),
    ]
