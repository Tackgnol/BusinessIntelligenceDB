# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-17 08:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('CommonItems', '0003_auto_20170928_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ParentUser', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('RecentCategories', models.ManyToManyField(to='CommonItems.Category')),
            ],
        ),
        migrations.AlterModelOptions(
            name='supplier',
            options={'verbose_name_plural': 'Suppliers'},
        ),
    ]
