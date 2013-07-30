from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse


urlpatterns = patterns('',
    url(r'^$', 'alighi.views.alighi', name='alighi'),
    url(r'^ntoj/', 
        lambda request, url: redirect(reverse('alighintoj'))),
    url(r'^gratulon/$', 'alighi.views.gratulon', name='gratulon'),
    url(r'^alighintoj/$', 'alighi.views.alighintoj', name='alighintoj'),
)
