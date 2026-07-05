from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'currency')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "currency"]

        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ваш username"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Ваш email"
            }),
            "currency": forms.Select(attrs={
                "class": "form-select"
            }),
        }