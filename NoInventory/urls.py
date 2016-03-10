from django.conf.urls import patterns, url
from NoInventory import views
from NoInventory.views import *

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^inventarios$', views.inventarios, name='inventarios'),
        url(r'^inventario/(?P<id_inventario>[\w\-]+)/$', views.inventario, name='inventario'),
        url(r'^addToInventario/(?P<id_inventario>[\w\-]+)/(?P<id_item>[\w\-]+)/$', views.addToInventario, name='addToInventario'),
        url(r'^items$', views.items, name='items'),
        #url(r'^prueba$', views.prueba, name='prueba'),
        #url(r'^nuevoItem/$', views.nuevoItem, name='nuevoItem'),
        #url(r'^nuevoInventario/$', views.nuevoInventario, name='nuevoInventario'),
        #url(r'^borrarItem/(?P<id>[\w\-]+)/$', views.borrarItem, name='borrarItem'),
        url(r'^borrarItem/$', views.borrarItem,name='borrarItem'),
        (r'^nuevoItem/$', ItemCreator.as_view()),
        (r'^modificarItem/(?P<id_item>[\w\-]+)/$',ItemUpdater.as_view()),
        (r'^nuevoInventario/$', InventoryCreator.as_view()),
        (r'^modificarInventario/(?P<id_inventario>[\w\-]+)/$',InventoryUpdater.as_view()),
        )
