from django.conf.urls import url
from .views import LoadCategories, AllCategories, updateSubCategory, deleteSubCategory, newSubCategory, getCategories
app_name = 'CommonItems'

urlpatterns = [
    url(r'^Load/$', LoadCategories.as_view(), name='Load'),
    url(r'^Categories/$', AllCategories.as_view(), name='Categories'),
    url(r'^$', AllCategories.as_view(), name='Categories'),
    url(r'ajax/EditCategory', updateSubCategory, name=None),
    url(r'ajax/DeleteCategory', deleteSubCategory, name=None),
    url(r'ajax/CreateCategory', newSubCategory, name=None),
    url(r'ajax/getCategoryParents', getCategories, name=None),
]