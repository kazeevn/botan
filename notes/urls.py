from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('notes.views',
    url(r'^$', 'index'),
    url(r'^(?P<note_id>\d+)/$', 'detail'),
    url(r'^(?P<note_id>\d+)/(?P<par_id>\d+)/$', 'paragraph'),
    url(r'^(?P<note_id>\d+)/(?P<par_id>\d+)/edit/$', 'paragraph_edit'),
    url(r'^(?P<note_id>\d+)/(?P<par_id>\d+)/commit/$', 'commit'),
    )
