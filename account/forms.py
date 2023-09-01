from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(required=True)
    phone_no = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'name', 'phone_no')

from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Phone Number')