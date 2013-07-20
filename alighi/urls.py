from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'alighi.views.alighi', name='alighi'),
    url(r'^gratulon/$', 'alighi.views.gratulon', name='gratulon'),
    url(r'^alighintoj/$', 'alighi.views.alighintoj', name='alighintoj'),
)
