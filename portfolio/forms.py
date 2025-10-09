# portfolio/forms.py

from django import forms
from .models import ContactSubmission

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'message']
        # --- UPDATE THIS WIDGETS SECTION ---
        widgets = {
            'name': forms.TextInput(attrs={'required': True, 'placeholder': ' '}),
            'email': forms.EmailInput(attrs={'required': True, 'placeholder': ' '}),
            'subject': forms.TextInput(attrs={'required': True, 'placeholder': ' '}),
            'message': forms.Textarea(attrs={'rows': 5, 'required': True, 'placeholder': ' '}),
        }