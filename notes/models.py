from django.db import models

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
  def __unicode__(self):
    return self.text

