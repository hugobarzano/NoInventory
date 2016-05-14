from django.conf.urls import patterns, include, url
from django.contrib import admin
from registration.backends.simple.views import RegistrationView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'NoInventoryProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('NoInventory.urls')),

)
urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
