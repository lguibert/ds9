# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0003_auto_20141106_2257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analysis',
            name='typegalaxy',
        ),
    ]
