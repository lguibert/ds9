# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ds9s', '0005_analysis_typegalaxy'),
    ]

    operations = [
        migrations.CreateModel(
            name='Identifications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('redshift', models.DecimalField(max_digits=19, decimal_places=10)),
                ('contamined', models.BooleanField(default=False)),
                ('galaxy', models.ForeignKey(to='ds9s.Galaxy')),
                ('galaxytype', models.ForeignKey(to='ds9s.GalaxyType')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='analysis',
            name='typegalaxy',
        ),
        migrations.RemoveField(
            model_name='galaxy',
            name='generated',
        ),
        migrations.AddField(
            model_name='galaxy',
            name='galaxytype',
            field=models.ManyToManyField(to='ds9s.GalaxyType', through='ds9s.Identifications'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='galaxytype',
            name='galaxys',
            field=models.ManyToManyField(related_name=b'galaxytype_galaxys_iden', through='ds9s.Identifications', to='ds9s.Galaxy'),
            preserve_default=True,
        ),
    ]
