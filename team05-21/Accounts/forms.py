from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


#This file edits the default UserCreationForm provided by Django, it can be used to add new fields to the registration process

User = get_user_model() 

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
