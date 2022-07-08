from django import forms
from django.db import models
#from .models import Author, Journal, Reference, ReferenceAuthor, ScientificName, LithoUnit, ChronoUnit, ScientificNameAuthor, ReferenceTaxon, ReferenceTaxonSpecimen
from .models import DolfinBox
from django.forms import ModelForm, inlineformset_factory, modelformset_factory

class DolfinBoxForm(ModelForm):
    class Meta:
        model = DolfinBox
        fields = ['dolfin_image','coords_str','boxname','boxcolor']