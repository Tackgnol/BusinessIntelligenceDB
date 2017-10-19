# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from CommonItems.models import Supplier, SubCategory

from django.db import models

# Create your models here.



class Insight(models.Model):
    Name = models.CharField(max_length=100)
    Details = models.CharField(max_length=1000, null=True, blank=False)
    Supplier = models.ForeignKey(Supplier)
    Categories = models.ManyToManyField(SubCategory)
    ChargeInvolved = models.BooleanField()
    Price = models.DecimalField(decimal_places=2, max_digits=10)
    Views = models.BigIntegerField(editable=False, default=0)

    def __str__(self):
        return self.Name

class Rating(models.Model):
    Insight = models.ForeignKey(Insight)
    Author = models.ForeignKey(User)
    Text = models.CharField(max_length=100)
    Rating = models.IntegerField(
        validators=(
            MaxValueValidator(5),
            MinValueValidator(1)
        )
    )


