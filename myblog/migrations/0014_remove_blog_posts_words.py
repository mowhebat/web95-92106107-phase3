# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-19 05:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0013_blog_posts_words'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='posts_words',
        ),
    ]
