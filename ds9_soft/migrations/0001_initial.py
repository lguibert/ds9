# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('ID_USER', models.IntegerField(serialize=False, primary_key=True)),
                ('EMAIL_USER', models.EmailField(max_length=254)),
                ('PASSWORD_USER', models.CharField(max_length=100)),
                ('FIRSTNAME_USER', models.CharField(max_length=75)),
                ('LASTNAME_USER', models.CharField(max_length=75)),
                ('REGISTRATIONDATE_USER', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
