from django import forms
from django.forms import ModelForm
from .models import Document

class DocumentForm(forms.ModelForm):
	class Meta:
		model = Document
		fields = ('description','document',)
