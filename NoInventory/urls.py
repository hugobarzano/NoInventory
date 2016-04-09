from django.conf.urls import patterns, url
from NoInventory import views
from NoInventory.views import *

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^catalogos$', views.catalogos, name='catalogos'),
        url(r'^catalogo/(?P<id_catalogo>[\w\-]+)/$', views.catalogo, name='catalogo'),
        url(r'^addToCatalogo/(?P<id_catalogo>[\w\-]+)/(?P<id_item>[\w\-]+)/$', views.addToCatalogo, name='addToCatalogo'),
        url(r'^items$', views.items, name='items'),
        #url(r'^prueba$', views.prueba, name='prueba'),
        #url(r'^nuevoItem/$', views.nuevoItem, name='nuevoItem'),
        #url(r'^nuevoCatalogo/$', views.nuevoCatalogo, name='nuevoCatalogo'),
        #url(r'^borrarItem/(?P<id>[\w\-]+)/$', views.borrarItem, name='borrarItem'),
        url(r'^borrarItem/$', views.borrarItem,name='borrarItem'),
        (r'^nuevoItem/$', ItemCreator.as_view()),
        (r'^modificarItem/(?P<id_item>[\w\-]+)/$',ItemUpdater.as_view()),
        (r'^nuevoCatalogo/$', CatalogoCreator.as_view()),
        (r'^modificarCatalogo/(?P<id_catalogo>[\w\-]+)/$',CatalogoUpdater.as_view()),
        (r'^preferencias/$',Preferencias.as_view()),
        #url(r'^preferencias/$',views.preferencias,name='preferencias'),
        url(r'^catalogosJson/$',views.catalogosJson,name='catalogosJson'),
        url(r'^itemsJson/$',views.itemsJson,name='itemsJson'),
        url(r'^deleteItems/$',views.deleteItems,name='deleteItems'),
        url(r'^deleteInventorys/$',views.deleteInventorys,name='deleteInventorys'),
        url(r'^addItemFromQr/$',views.addItemFromQr,name='addItemFromQr'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^androidLogin/$', views.androidLogin, name='androidLogin'),
        url(r'^androidRegister/$', views.androidRegister, name='androidRegister'),
        (r'^AndroidNuevoItem/$', AndroidItemCreator.as_view()),


        )
