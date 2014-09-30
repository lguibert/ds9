# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9_soft', '0002_auto_20140930_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='EMAIL_USER',
            field=models.EmailField(unique=True, max_length=254),
        ),
    ]
