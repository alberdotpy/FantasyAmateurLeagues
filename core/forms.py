# core/forms.py

from django import forms
from .models import League
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LeagueCreationForm(forms.ModelForm):
    class Meta:
        model = League
        fields = ['name', 'sport', 'country']
