# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0002_auto_20141008_2049'),
    ]

    operations = [
        migrations.RenameField(
            model_name='analysis',
            old_name='reshift',
            new_name='redshift',
        ),
        migrations.AlterField(
            model_name='galaxy',
            name='parfolder',
            field=models.ForeignKey(to='ds9s.ParFolder'),
        ),
    ]
