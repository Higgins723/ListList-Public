# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-26 04:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20160325_2215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='media',
        ),
    ]
