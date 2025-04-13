

from django import forms
from managements.models import ContactUs


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = '__all__'
        exclude = ('seen',)
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کامل'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تماس با فرمت 09'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'موضوع'}),
            'user_message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'پیام', 'rows': '6'}),
        }

