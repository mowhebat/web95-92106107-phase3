# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-12 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0002_auto_20170712_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.AutoField(error_messages={'required': 'id needed'}, primary_key=True, serialize=False),
        ),
    ]
