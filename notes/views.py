from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from notes.models import Note, Paragraph
import datetime

def detail(request, note_id):
  n = get_object_or_404(Note, pk=note_id)
  return render_to_response('notes/detail.html', {'note': n})

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
  p = get_object_or_404(Note, pk=par_id)
  return HttpResponse(p.text)

def paragraph_rendered(request, note_id, par_id):
  n = get_object_or_404(Note, pk=note_id)
  p = get_object_or_404(Note, pk=par_id)
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
