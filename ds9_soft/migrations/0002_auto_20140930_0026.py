# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9_soft', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='ID_USER',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
