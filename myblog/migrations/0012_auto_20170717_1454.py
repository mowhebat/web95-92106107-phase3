# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-17 14:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0011_auto_20170713_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
