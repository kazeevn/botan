from django.db import models
from django import forms
from creoleparser import text2html

class Note(models.Model):
  title = models.CharField(max_length = 100)
  author = models.CharField(max_length = 100)
  last_edit = models.DateTimeField('last edit')
  def __unicode__(self):
    return self.title

class Paragraph(models.Model):
  is_rendered = False
  title = models.CharField(max_length = 100)
  note = models.ForeignKey(Note)
  rendered = models.CharField(max_length = 2000)
  text = models.CharField(max_length = 2000)
  last_edit = models.DateTimeField('last edit')
  #TODO(kazeevn) add creation time
  #TODO(kazeevn) add proper constructor

  def render(self):
    #TODO(kazeevn) check creoleparser security!!
    try:
      self.rendered=text2html(self.text)
      self.is_rendered=True
    except:
      self.rendered=("Error while rendering!")
      self.is_rendered=False

  def __unicode__(self):
    return self.text

  class EditForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(max_length=2000, widget=forms.Textarea)


