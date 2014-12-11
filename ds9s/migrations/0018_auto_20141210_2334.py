# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0017_auto_20141118_1807'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='analysis',
            options={'permissions': (('view_allreviews', 'Can see all reviews'),)},
        ),
        migrations.AlterModelOptions(
            name='identifications',
            options={'permissions': (('view_allreviews', 'Can see all reviews'),)},
        ),
    ]
