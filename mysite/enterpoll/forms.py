from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import custom_validators
from .models import Poll, Choice, Comment


class UserCreationForm(UserCreationForm):

	def clean(self):
		cleaned_data = super().clean()
		custom_validators.forbidden_words(cleaned_data['username'])
		return cleaned_data


class PollModelForm(forms.ModelForm):

	class Meta:
		model = Poll
		fields = ['title', 'description']
		widgets = {
			'title': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
			'description': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
		}


class CommentModelForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ['text']
		widgets = {
			'text': forms.Textarea(attrs={'cols': 40, 'rows': 2, 'required': True})
		}
		labels = {
			'text': ''
		}
