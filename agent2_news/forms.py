### ✅ agent2_news/forms.py

from django import forms
from .models import NewsResource

class ResourceUploadForm(forms.ModelForm):
    class Meta:
        model = NewsResource
        fields = ['title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rule Title'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
