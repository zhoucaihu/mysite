from django.conf.urls import url
from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$',views.select,name='select'),
    url(r'^params/$',views.params,name='params'),
    url(r'^result/(?P<pk>[0-9]+)$',views.result,name='result')
]