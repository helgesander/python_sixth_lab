
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.forms import Form
from django import forms
from django.contrib import messages


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label="Логин", max_length=100)
    email = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def check(self):
        try:
            User.objects.get(username=self.username)
        except User.DoesNotExist:
            print("Пользователь с таким логином уже существует")

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password']
        )
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(label="Логин", max_length=100, error_messages={'empty' : 'Введите логин! '})
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput, error_messages={'empty': 'Введите пароль! '})



