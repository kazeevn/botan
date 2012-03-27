from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from notes.models import Note, Paragraph
import datetime

def detail(request, note_id):
  n = get_object_or_404(Note, pk=note_id)
  return render_to_response('notes/detail.html', {'note': n})

def paragraph_text(request, note_id, par_id):
  return HttpResponse(paragraph.text)

def paragraph_rendered(request, note_id, par_id):
  return HttpResponse(paragraph.rendered)

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
      return HttpResponseRedirect(reverse('notes.views.detail', args=(n.id,)))
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


