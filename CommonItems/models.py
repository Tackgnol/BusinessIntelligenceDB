# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Supplier(models.Model):
    Name = models.CharField(max_length=100)
    URL = models.URLField()
    Description = models.CharField(max_length=1000)
    def __str__(self):
        return self.Name
    def unicode(self):
        return self.Name
    class Meta:
        verbose_name_plural = "Suppliers"

class Category(models.Model):
    CategoryID = models.IntegerField()
    CategoryDescription = models.CharField(max_length=150)
    def __str__(self):
        return str(self.CategoryID) + " - " + self.CategoryDescription  
    class Meta:
        verbose_name_plural = "Categories" 

class SubCategory(models.Model):
    CategoryID = models.IntegerField()
    CategoryDescription = models.CharField(max_length=1000)
    Parent = models.ForeignKey(Category)

    def __str__(self):
        return str(self.CategoryID) + " - " + self.CategoryDescription
    def unicode(self):
        return str(self.CategoryID) + " - " + self.CategoryDescription
    class Meta:
        verbose_name_plural = "SubCategories"

class UserProfile(models.Model):
    ParentUser = models.OneToOneField(User)
    RecentCategories = models.ManyToManyField(SubCategory)
    