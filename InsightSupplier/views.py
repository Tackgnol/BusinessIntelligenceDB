# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.contrib.auth.models import User
from django.core import serializers
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.http import HttpResponse, HttpResponseForbidden
from models import Insight, Supplier, SubCategory


class Welcome(TemplateView):
    template_name = "Index.html"

class AllInsightsSources(TemplateView):
    template_name = "SupplierInsight/Index.html"

class CategoryOverview(DetailView):
    template_name = "SupplierInsight/Index.html"
    model = SubCategory

def getInsightSuppliers(request):
    sortOptions = { 
        'Alphabetically': 'Name',
        'Price': 'Price',
        'Rating': 'Supplier',
        'Views': 'Views'
    }
    if request.method == "GET":
        searchTerm = request.GET['searchField']
        chargeInvolved = request.GET['costInvolved'] 

        if chargeInvolved != u'true':
            chargeInvolved = False
        else:
            chargeInvolved = True
        sortBy = request.GET['sortBy']

        if searchTerm == None:
            dataSet = Insight.objects.filter(ChargeInvolved = chargeInvolved).order_by(sortOptions[sortBy])
        else:
            dataSet = Insight.objects.filter(Name__icontains = searchTerm, ChargeInvolved = chargeInvolved).order_by(sortOptions[sortBy])
        inclSupplier = []
        for row in dataSet:
            inclSupplier.append({
                "PK": row.pk,
                "Name": row.Name,
                "Supplier": row.Supplier.URL,
                "ChargeInvolved": row.ChargeInvolved,
                "Price": float(row.Price),
                "Views": row.Views
            })
        data = json.dumps(inclSupplier)


        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )

    else:
        return HttpResponseForbidden();
