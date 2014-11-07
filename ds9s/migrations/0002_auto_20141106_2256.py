# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='analysis',
            old_name='typegalaxy',
            new_name='typeeeegalaxy',
        ),
    ]
