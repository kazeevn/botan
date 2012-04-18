from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from notes.models import Note, Paragraph, UploadForm
from django.views.generic.simple import direct_to_template
import datetime
import re
import mimetypes

#TODO(kazeevn) Move to a separate backend
from google.appengine.ext import blobstore

def detail(request, note_id):
  n = get_object_or_404(Note, pk=note_id)
  return render_to_response('notes/detail.html', {'note': n})

def serve_image(request, note_id, par_id):
  p = get_object_or_404(Paragraph, pk=par_id)
#  import pdb; pdb.set_trace();
  response = HttpResponse("No image")
  response[blobstore.BLOB_KEY_HEADER] = p.blob_key
  response['Content-Type'] = ''
  return response

# Eats WSGI requsts returns BlobKey
# Security:
# TODO(kazeevn) Can a client send a spoofed blobkey?
# TODO(kazeevn) Check if our regexp can be fooled.
def get_blob_key(request):
  try:
    return re.search('(?<=Content-Type: message/external-body; blob-key=").+?(?=")',
      request.META['wsgi.input'].getvalue()).group()
  except:
    return None
  
def upload(request, note_id, par_id):
  p = get_object_or_404(Paragraph, pk=par_id)
  if request.method == 'POST':
    old_key = p.blob_key
    p.blob_key = get_blob_key(request)
    info = blobstore.BlobInfo(blobstore.BlobKey(p.blob_key))
    if re.match("image/", info.content_type) is None:
        blobstore.delete_async(p.blob_key)
        p.blob_key = old_key
        return HttpResponseForbidden("An image, please!")
    blobstore.delete_async(old_key)
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
    return HttpResponse("I eat only POST")


def paragraph_text(request, note_id, par_id):
  n = get_object_or_404(Note, pk=note_id)
  p = get_object_or_404(Paragraph, pk=par_id)
  return HttpResponse(p.text)

def paragraph_rendered(request, note_id, par_id):
  n = get_object_or_404(Note, pk=note_id)
  p = get_object_or_404(Paragraph, pk=par_id)
  return HttpResponse(p.rendered)

def paragraph_edit(request, note_id, par_id):
  n = get_object_or_404(Note, pk=note_id)
  try:
    p = Paragraph.objects.get(pk=par_id)
    form = Paragraph.EditForm({
        'title':p.title,
        'text':p.text})
  except Paragraph.DoesNotExist:
    form = Paragraph.EditForm()
    return render_to_response('notes/edit.html', {
      'error_message': "Paragraph you requested doesn't exist.\
      Please feel free to create it.",
      'form': form,
      'note_id':note_id,
      'par_id':0
      })

  return render_to_response('notes/edit.html', {'form': form,
      'paragraph':p,
      'note_id':note_id,
      'par_id':par_id
      })

def commit(request, note_id, par_id):
  n = get_object_or_404(Note, pk=note_id)
  if request.method == 'POST':
    form = Paragraph.EditForm(request.POST)
    if form.is_valid():
      try:
        p = Paragraph.objects.get(pk=par_id)
      except Paragraph.DoesNotExist:
        p = Paragraph()
        p.note = n
      p.text = form.cleaned_data['text']
      p.title = form.cleaned_data['title']
      p.last_edit = datetime.datetime.now()
      p.render()
      p.save()
      return HttpResponse(p.rendered)
    else:
      return render_to_response('notes/edit.html', {
          'error_message': "Please make your edit correct",
          'form': form,
          'note_id':note_id,
          'par_id':par_id
          })
  else:
    return render_to_response('notes/edit.html', {
        'error_message': "Please use POST to make edits",
        'form': form,
        'note_id':note_id,
        'par_id':par_id
        })
