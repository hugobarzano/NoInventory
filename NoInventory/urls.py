from django.conf.urls import patterns, url
from NoInventory import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^nuevoItem/$', views.nuevoItem, name='nuevoItem'),
        )
