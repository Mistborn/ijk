from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'alighi.views.alighi', name='alighi'),
)