# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0010_fits'),
    ]

    operations = [
        migrations.AddField(
            model_name='fits',
            name='file_field',
            field=models.FileField(null=True, upload_to=b'fits/'),
            preserve_default=True,
        ),
    ]
