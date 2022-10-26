
from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.Form):
    username = forms.CharField(label="Логин", max_length=100)
    email = forms.EmailField(label="Email", max_length=100)
    password = forms.PasswordInput()

