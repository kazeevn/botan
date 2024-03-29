from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic import ListView, DetailView

from models import Note
from notes.views import NoteListView, NoteDetailView

urlpatterns = patterns('notes.views',
    url(r'^$', NoteListView.as_view(), name='notes_root'),
    url(r'^(?P<pk>\d+)/$', NoteDetailView.as_view(), name='notes_detail'),
    url(r'^preview/$', 'preview'),
    url(r'^(?P<note_id>\d+)/(?P<par_id>\d+)/text$', 'paragraph_text'),
    url(r'^(?P<note_id>\d+)/(?P<par_id>\d+)/upload$', 'upload'),
    url(r'^(?P<note_id>\d+)/(?P<par_id>\d+)/image$', 'serve_image'),
    url(r'^(?P<note_id>\d+)/(?P<par_id>\d+)/rendered$', 'paragraph_rendered'),
    url(r'^(?P<note_id>\d+)/(?P<par_id>\d+)/commit/$', 'commit'),
    url(r'^(?P<note_id>\d+)/add/$', 'add'),
    url(r'^add/$', 'add_note'),
    )
