# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ds9s', '0005_users_photo_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='PHOTO_USER',
            field=models.ImageField(null=True, upload_to=b'/user/'),
        ),
    ]
