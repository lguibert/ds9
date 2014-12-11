# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0018_auto_20141210_2334'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='analysis',
            options={'permissions': (('view_allAnalysis', 'Can see all analysis'),)},
        ),
        migrations.AlterModelOptions(
            name='identifications',
            options={'permissions': (('view_allIdentifications', 'Can see all identifications'),)},
        ),
    ]
