# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-12 18:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0006_auto_20170712_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='count',
            field=models.IntegerField(blank=True, default=models.AutoField(primary_key=True, serialize=False)),
        ),
    ]