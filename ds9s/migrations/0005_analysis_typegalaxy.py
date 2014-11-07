# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0004_remove_analysis_typegalaxy'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='typegalaxy',
            field=models.ForeignKey(default=1, to='ds9s.GalaxyType'),
            preserve_default=False,
        ),
    ]
