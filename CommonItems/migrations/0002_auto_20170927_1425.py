# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 12:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CommonItems', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'verbose_name_plural': 'SubCategories'},
        ),
        migrations.RenameField(
            model_name='subcategory',
            old_name='Category',
            new_name='Parent',
        ),
    ]