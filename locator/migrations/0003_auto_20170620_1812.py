# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-20 18:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0002_fingerprintedlocation_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fingerprintedlocation',
            name='image',
        ),
        migrations.AddField(
            model_name='floorplan',
            name='image',
            field=models.ImageField(default=None, upload_to=''),
            preserve_default=False,
        ),
    ]
