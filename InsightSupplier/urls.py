from django.conf.urls import url
from .views import AllInsightsSources, getInsightSuppliers, CategoryOverview
app_name = 'InsightSupplier'

urlpatterns = [
    url(r'^$', AllInsightsSources.as_view(), name='Sources'),
    url(r'ajax/getInsights', getInsightSuppliers, name=None),
    url(r'/(?P<pk>\d+)/$', CategoryOverview.as_view(), name='Category'),
]