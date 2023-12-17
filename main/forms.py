from django import forms
from django.forms import ModelForm
from signup.models import Messages

class ImageForm(ModelForm):
    class Meta:
        model = Messages
        fields = ('incoming', 'outgoing', 'type', 'image', 'message')

        widgets = {
            '': forms.TextInput(attrs={'class':'form-control', 'hidden':'hidden'}),
            '': forms.TextInput(attrs={'class':'form-control', 'hidden':'hidden'}),
            '' : forms.TextInput(attrs={'class':'form-control', 'hidden':'hidden'}),
            'Image' : forms.ImageField(),
            '' : forms.TextInput(attrs={'class':'form-control', 'hidden':'hidden'}),
        }
