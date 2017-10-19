from __future__ import unicode_literals
from validators import makeDataFrame
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, FormView, ListView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseForbidden
from models import SubCategory, Category
from forms import FileForm
import json




def getCategories(request):
    if request.method == 'GET':
        searchTerm = request.GET.get('search')
        if searchTerm == None:
            searchTerm = "";
        response_data = {}
        response_data['results'] = []
        responseCategories = Category.objects.all()
        for element in responseCategories:
            if searchTerm.upper() in str(element):
                response_data['results'].append({'id':element.pk, 'text':str(element.CategoryID) + ' - ' + element.CategoryDescription })
                
        response_data['pagination'] = {'more':True}

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )



def newSubCategory(request):
    if request.method == 'POST':
        response_data = {}
        response_data['result'] = True
        newCatId = request.POST.get('createdCatId')
        newCatDesc = request.POST.get('createdCatName').upper()
        newCatParent = request.POST.get('CategoryParent')
        if  SubCategory.objects.filter(CategoryID=newCatId).count() > 0:
            response_data['result'] = False
            response_data['msg'] = 'Category of this code already exists, please specify a different code'
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"   
            )

        try:
            newCatParent=Category.objects.get(pk=newCatParent)
            newSubCat = createSubCategory(newCatId, newCatDesc, newCatParent)
            newSubCat.save()
            response_data['Category'] = str(newCatParent)
            response_data['SubCategory'] = str(newSubCat)
            response_data['pk'] = newSubCat.pk
        except:
            response_data['result'] = False
            response_data['msg'] = 'Failed to create the subcategory, please try again later'
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"   
        )



def updateSubCategory(request):
    if request.method == 'POST':
        itemPK = request.POST.get('changePK')
        newCatId = request.POST.get('newCatId')
        newCatDesc = request.POST.get('newCatDesc')

        thisCategory = get_object_or_404(SubCategory, pk=itemPK)
        thisCategory.CategoryID = newCatId
        thisCategory.CategoryDescription = newCatDesc
        thisCategory.save()
        response_data = {}
        response_data['result'] = 'Create post successful!'
        response_data['catID'] = thisCategory.CategoryID
        response_data['catDesc'] = thisCategory.CategoryDescription

        return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
        )
    else:
        return HttpResponseForbidden()

def deleteSubCategory(request):
    if request.method == 'POST':
        itemPK = request.POST.get('deletePK')

        thisCategory = get_object_or_404(SubCategory, pk=itemPK)

        thisCategory.delete()
        response_data = {}
        response_data['message'] = 'Delete SubCat successful!'
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

class LoadCategories(FormView):
    template_name = "CommonItems/LoadCategories.html"
    form_class = FileForm
    success_url = "Index"
    def form_valid(self, form):
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        file = form.cleaned_data['file']
        df = makeDataFrame(file)
        for index, row in df.iterrows():
            category = createOrGetCategory(number = row[u'Category Level 1 Code'], text = row[u'Category Level 1 Name'])
            createSubCategory(number=row[u'Category Level 2 Code'], text = row[u'Category Level 2 Name'], cat=category)
        return super(LoadCategories, self).form_valid(form)

class AllCategories(ListView):
    template_name = "CommonItems/AllCategories.html"
    queryset = SubCategory.objects.order_by('CategoryID')

def createOrGetCategory(number, text):
    try:
        cat =Category.objects.get(CategoryID=number)
    except ObjectDoesNotExist:
        cat = Category(CategoryID=number, CategoryDescription=text)
        cat.save() 
    return cat

def createSubCategory(number, text, cat):
    subCat = SubCategory(CategoryID = number, CategoryDescription=text, Parent=cat)
    subCat.save()
    return subCat


