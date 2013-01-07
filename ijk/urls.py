from django.conf.urls import patterns, include, url
from django.conf import settings

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

# Rich text editor for flatpages
class EditorMedia:
    js = (
        'https://ajax.googleapis.com/ajax/libs/dojo/1.6.0/dojo/dojo.xd.js',
        '/static/js/editor.js',
    )
    css = {'all': ('/static/css/editor.css',)}

# Force flatpages to default to the current site
from django.forms import ModelMultipleChoiceField
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages import admin as flatadmin, forms as flatforms
from django.contrib.sites.models import Site
class NewFlatpageForm(flatforms.FlatpageForm):
    sites = ModelMultipleChoiceField(queryset=Site.objects.all(),
        initial=[Site.objects.get_current()])
class NewFlatPageAdmin(flatadmin.FlatPageAdmin):
    form = NewFlatpageForm
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, NewFlatPageAdmin, Media=EditorMedia)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ijk.views.home', name='home'),
    # url(r'^ijk/', include('ijk.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^alighi/', include('alighi.urls')),
    url(r'^bazo/', 'alighi.views.bazo'),
    url('^', include('django.contrib.flatpages.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
