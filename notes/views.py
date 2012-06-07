from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from notes.models import Note, Paragraph, UploadForm
from django.views.generic.simple import direct_to_template
import datetime
import re
import mimetypes

#TODO(kazeevn) Make it a separate backend
from google.appengine.ext import blobstore

def serve_image(request, note_id, par_id):
  p = get_object_or_404(Paragraph, pk=par_id)
  response = HttpResponse()
  info = blobstore.BlobInfo(blobstore.BlobKey(p.blob_key))
  response['Content-Type'] = info.content_type
  response[blobstore.BLOB_KEY_HEADER] = p.blob_key
  return response

# Eats WSGI requsts, returns BlobKey
# Security:
# TODO(kazeevn) Can a client send a spoofed blobkey?
# TODO(kazeevn) Use a good parser. Shall we import webapp?
def get_blob_key(request):
  req = request.META['wsgi.input'].getvalue()
  res = re.search('(?<=blob-key=)[\w_\-"]+',req)
  if res is not None:
    return res.group().replace('"', '')
  else:
    return None
  
def upload(request, note_id, par_id):
  p = get_object_or_404(Paragraph, pk=par_id)
  if request.method == 'POST':
    submitted_key = get_blob_key(request)
    if submitted_key is None:
      return HttpResponseForbidden("An ugly person you are. Please,\
          don't feed me with invalid headrs. This functionality\
          is mission-crtical, you know.")
    info = blobstore.BlobInfo(blobstore.BlobKey(submitted_key))
    if re.match("image/", info.content_type) is None:
        blobstore.delete_async(submitted_key)
        return HttpResponseForbidden("An image, please!")
    blobstore.delete_async(p.blob_key)
    p.blob_key = submitted_key
    p.last_edit = datetime.datetime.now()
    p.save()
    view_url = reverse('notes.views.serve_image', args=[note_id, par_id])
    return HttpResponseRedirect(view_url)
  upload_url = reverse('notes.views.upload', args=[note_id, par_id])
  upload_url_rpc = blobstore.create_upload_url_async(upload_url)
  form = UploadForm()
  upload_url = upload_url_rpc.get_result()
  return direct_to_template(request, 'notes/upload.html',
      {'form': form, 'upload_url': upload_url})


# TODO(kazeevn) consider moving to client
# there is a library
def preview(request):
  if request.method == 'POST':
    form = Paragraph.EditForm(request.POST)
    if form.is_valid():
      p = Paragraph()
      p.text = form.cleaned_data['text']
      p.title = form.cleaned_data['title']
      p.last_edit = datetime.datetime.now()
      p.render()
      return HttpResponse(p.rendered)
    else:
      return HttpResponse("Incorrect input")
  else:
    return HttpResponseForbidden("I eat only POST")


def paragraph_text(request, note_id, par_id):
  n = get_object_or_404(Note, pk=note_id)
  p = get_object_or_404(Paragraph, pk=par_id)
  return HttpResponse(p.text)

def paragraph_rendered(request, note_id, par_id):
  n = get_object_or_404(Note, pk=note_id)
  p = get_object_or_404(Paragraph, pk=par_id)
  return HttpResponse(p.rendered)

def add(request, note_id):
  n = get_object_or_404(Note, pk=note_id)
  if request.method == 'POST':
    form = Paragraph.EditForm(request.POST)
    if form.is_valid():
      p = Paragraph()
      p.note = n
      p.text = form.cleaned_data['text']
      p.title = form.cleaned_data['title']
      p.last_edit = datetime.datetime.now()
      p.render()
      p.save()
      return HttpResponseRedirect(reverse('notes_detail', args=[n.id]))
    else:
      return HttpResponseForbidden("Invalid data.")
  else:
    return HttpResponseForbidden("POST, please!")

def add_note(request):
  if request.method == 'POST':
    form = Note.AddForm(request.POST)
    if form.is_valid():
      n = Note()
      n.author = form.cleaned_data['author']
      n.title = form.cleaned_data['title']
      n.last_edit = datetime.datetime.now()
      n.save()
      # TODO(kazeevn) redo it in a better style
      return HttpResponse(r"<li><a href=/notes/{0}>{1}</a></li>".format(n.id, n.title))
    else:
      return HttpResponseForbidden("Invalid data.")
  else:
    return HttpResponseForbidden("POST, please!")


def commit(request, note_id, par_id):
  n = get_object_or_404(Note, pk=note_id)
  if request.method == 'POST':
    form = Paragraph.EditForm(request.POST)
    if form.is_valid():
      p = get_object_or_404(Paragraph, pk=par_id)
      p.text = form.cleaned_data['text']
      p.title = form.cleaned_data['title']
      p.last_edit = datetime.datetime.now()
      p.render()
      p.save()
      return HttpResponse(p.rendered)
    else:
      return HttpResponseForbidden("Invalid data.")
  else:
    return HttpResponseForbidden("POST, please!")
