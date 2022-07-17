from django import forms
from django.db import models
#from .models import Author, Journal, Reference, ReferenceAuthor, ScientificName, LithoUnit, ChronoUnit, ScientificNameAuthor, ReferenceTaxon, ReferenceTaxonSpecimen
from dolfinrest.models import DolfinBox, DolfinUser
from django.forms import ModelForm, inlineformset_factory, modelformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.conf import settings
#class JournalForm(ModelForm):
#    class Meta:
#        model = Journal
#        fields = ['title_k', 'title_e', 'publisher', 'since', 'issn']

class UserForm(forms.ModelForm):
    class Meta:
        model = DolfinUser
        fields = ['last_name', 'first_name','email']

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = DolfinUser
		fields = ["username", "email", "password1", "password2"]
		widgets = {
            'username': forms.TextInput(attrs={'size': 20,'placeholder':'사용자ID'}),
		}

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user