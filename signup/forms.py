from django import forms
from django.forms import ModelForm
from core.models import Users

class SignupForm(ModelForm):
    class Meta:
        model = Users
        fields = ('username', 'email', 'password', 'photo')

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username: '}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email Address: '}),
            'password' : forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password: '}),
        }
