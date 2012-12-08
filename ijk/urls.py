from django.conf.urls import patterns, include, url
from django.conf import settings

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ijk.views.home', name='home'),
    # url(r'^ijk/', include('ijk.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^alighi/', include('alighi.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
