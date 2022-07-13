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

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name','email', 'groups']

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user