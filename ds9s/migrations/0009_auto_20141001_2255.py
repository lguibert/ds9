# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0008_auto_20141001_0346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='role',
        ),
        migrations.DeleteModel(
            name='Roles',
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]
