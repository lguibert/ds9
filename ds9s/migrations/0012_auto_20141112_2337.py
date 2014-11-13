# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0011_auto_20141112_2334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emissionfeatures',
            name='emissionline',
        ),
        migrations.RemoveField(
            model_name='emissionfeatures',
            name='emissionlinefields',
        ),
        migrations.DeleteModel(
            name='EmissionFeatures',
        ),
    ]
