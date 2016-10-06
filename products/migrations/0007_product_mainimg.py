# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-31 04:23
from __future__ import unicode_literals

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_remove_product_media'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='mainimg',
            field=models.ImageField(null=True, upload_to=products.models.image_upload_to),
        ),
    ]
