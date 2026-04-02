from django import forms
from .models import PasswordEntry
from django.contrib.auth.models import User


class SignupForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") != cleaned.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match!")
        return cleaned


class PasswordEntryForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = PasswordEntry
        fields = ["password_name", "username", "password","notes", "confirm_password" ]
        widgets = {
            "password": forms.PasswordInput,
        }

    def clean(self):
        cleaned = super().clean()

        # Password match check
        if cleaned.get("password") != cleaned.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match!")

       
        return cleaned