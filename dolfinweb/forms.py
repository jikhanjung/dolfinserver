from django import forms
from django.db import models
#from .models import Author, Journal, Reference, ReferenceAuthor, ScientificName, LithoUnit, ChronoUnit, ScientificNameAuthor, ReferenceTaxon, ReferenceTaxonSpecimen
from dolfinrest.models import DolfinBox
from django.forms import ModelForm, inlineformset_factory, modelformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.conf import settings
#class JournalForm(ModelForm):
#    class Meta:
#        model = Journal
#        fields = ['title_k', 'title_e', 'publisher', 'since', 'issn']

