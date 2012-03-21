from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic import ListView
from models import Note

urlpatterns = patterns('notes.views',
    url(r'^$', ListView.as_view(
        model=Note,
        context_object_name="notes_list"
        )),
    url(r'^(?P<note_id>\d+)/$', 'detail'),
    url(r'^(?P<note_id>\d+)/(?P<par_id>\d+)/$', 'paragraph'),
    url(r'^(?P<note_id>\d+)/(?P<par_id>\d+)/edit/$', 'paragraph_edit'),
    url(r'^(?P<note_id>\d+)/(?P<par_id>\d+)/commit/$', 'commit'),
    )
