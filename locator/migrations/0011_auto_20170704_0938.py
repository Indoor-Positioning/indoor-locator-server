# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-04 09:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0010_userlocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlocation',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='userlocation',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
