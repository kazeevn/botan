from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from notes.models import Note, Paragraph

def index(request):
  latest_notes_list = Note.objects.all().order_by('-last_edit')[:5]
  return render_to_response('notes/index.html', {'latest_notes_list': latest_notes_list})

def detail(request, note_id):
  n = get_object_or_404(Note, pk=note_id)
  return render_to_response('notes/detail.html', {'note': n})

def paragraph(request, note_id, par_id):
  return HttpResponse("Note %s, paragraph %s" % (note_id, par_id))

def paragraph_edit(request, note_id, par_id):
  n = get_object_or_404(Note, pk=note_id)
  p = get_object_or_404(Paragraph, pk=par_id)
  return render_to_response('notes/edit.html', {'paragraph':p, 'note': n},
      context_instance=RequestContext(request))

# TODO (herer
def commit(request, note_id, par_id):
  n = get_object_or_404(Note, pk=note_id)
  p = get_object_or_404(Paragraph, pk=par_id)
  p.text =   
