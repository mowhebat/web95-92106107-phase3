# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-19 12:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0016_remove_blog_posts_words'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='posts_words',
            field=models.CharField(default='', max_length=1000),
        ),
    ]