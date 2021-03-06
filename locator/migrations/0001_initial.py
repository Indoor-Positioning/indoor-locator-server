# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-20 18:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FingerPrint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('magnetic_x', models.FloatField()),
                ('magnetic_y', models.FloatField()),
                ('magnetic_z', models.FloatField()),
                ('orientation_x', models.FloatField()),
                ('orientation_y', models.FloatField()),
                ('orientation_z', models.FloatField()),
                ('wifi_rssi', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='FingerPrintedLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_coord', models.FloatField()),
                ('y_coord', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='FloorPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PointOfInterest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('x_coord', models.FloatField()),
                ('y_coord', models.FloatField()),
                ('floor_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locator.FloorPlan')),
            ],
        ),
        migrations.AddField(
            model_name='fingerprintedlocation',
            name='floor_plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locator.FloorPlan'),
        ),
        migrations.AddField(
            model_name='fingerprint',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locator.FingerPrintedLocation'),
        ),
    ]
