from django import forms
from django.contrib.auth import get_user_model


class LoginForm(forms.Form):
    """user login form"""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    # selected_project = forms.Select()
    # selected_project = forms.CharField(widget=forms.CheckboxSelectMultiple)
