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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('EMAIL_USER', models.EmailField(unique=True, max_length=254)),
                ('PASSWORD_USER', models.CharField(max_length=100)),
                ('FIRSTNAME_USER', models.CharField(max_length=76)),
                ('LASTNAME_USER', models.CharField(max_length=75)),
                ('REGISTRATIONDATE_USER', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
