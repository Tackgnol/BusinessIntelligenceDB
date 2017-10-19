# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import Category, SubCategory, Supplier
from django.contrib import admin

# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Supplier)
