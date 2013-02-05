from django.conf.urls import patterns, include, url
from django.conf import settings
from django.shortcuts import redirect

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ijk.views.home', name='home'),
    # url(r'^ijk/', include('ijk.foo.urls')),

    # all our urls end in slashes
    url(r'^(?P<url>.*[^/])$',
        lambda request, url: redirect('/'+url.strip('/')+'/')),
    # actually we want to call the admin mastrumilo
    url(r'^admin(?P<url>.*)$',
        lambda request, url: redirect('/mastrumilo'+url)),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^mastrumilo/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^mastrumilo/', include(admin.site.urls)),

    url(r'^alighi/', include('alighi.urls')),
    url('^', include('django.contrib.flatpages.urls')),
)

if settings.DEBUG:
    urlpatterns = (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +
        staticfiles_urlpatterns() +
        urlpatterns)
