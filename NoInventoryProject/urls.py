from django.conf.urls import patterns, include, url
from django.contrib import admin
from registration.backends.simple.views import RegistrationView



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'NoInventoryProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^noinventory/', include('NoInventory.urls')),
)
