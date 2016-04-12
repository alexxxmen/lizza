# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-12 15:13
from __future__ import unicode_literals

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_auto_20160411_2023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='telephone',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_id',
        ),
        migrations.AddField(
            model_name='feedback',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, verbose_name=b'\xd0\x9d\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80 \xd1\x82\xd0\xb5\xd0\xbb\xd0\xb5\xd1\x84\xd0\xbe\xd0\xbd\xd0\xb0'),
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, verbose_name=b'\xd0\x9d\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80 \xd1\x82\xd0\xb5\xd0\xbb\xd0\xb5\xd1\x84\xd0\xbe\xd0\xbd\xd0\xb0'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_code',
            field=models.CharField(max_length=30, null=True, unique=True, verbose_name=b'product_id'),
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name=b'\xd0\x9f\xd0\xbe\xd1\x87\xd1\x82\xd0\xb0'),
        ),
    ]