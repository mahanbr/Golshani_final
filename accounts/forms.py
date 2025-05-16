from django import forms
from .models import Account,UserDocument
from PIL import Image
from django.core.exceptions import ValidationError


class ProfileForm(forms.ModelForm):        

    class Meta:
        model = Account
        fields = '__all__'
        exclude = ('user', 'city', 'province', 'birthday', 'status', 'return_period', 'loan_type')
        

        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control  text-center form-select', 'required':''}),
            'chtype': forms.Select(attrs={'class': 'form-control  text-center form-select', 'required':''}),
            'postal_code': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'کد پستی', 'required':''}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ' تلفن ثابت بدون فاصله', 'required':''}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'آدرس', 'rows': '3', 'required':''}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'required':''}),
            'code_meli': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'کد ملی', 'required':''}),
            'jalali_birth': forms.TextInput(attrs={'class': 'form-control ', 'data-jdp': '', 'required':''},),
            'father_name': forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'نام پدر', 'required':''},),
        }




class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserDocument
        fields = ['cart_meli', 'shenas_name']
        exclude = ('user',)
        

    def clean_cart_meli(self):
        cart_meli = self.cleaned_data.get('cart_meli')
        self.validate_image_file(cart_meli)
        return cart_meli

    def clean_shenas_name(self):
        shenas_name = self.cleaned_data.get('shenas_name')
        self.validate_image_file(shenas_name)
        return shenas_name

    def validate_image_file(self, image):
        max_size = 1 * 1024 * 1024  # 1 MB
        valid_formats = ['JPEG', 'PNG']

        if image.size > max_size:
            raise ValidationError(f"Image size should not exceed {max_size / (1024 * 1024)} MB.")

        try:
            img = Image.open(image)
            img.verify()
            if img.format not in valid_formats:
                raise ValidationError(f"Only {', '.join(valid_formats)} formats are allowed.")
        except Exception:
            raise ValidationError("Invalid image file. Please upload a valid image.")

        img = Image.open(image)
        if img.width > 2000 or img.height > 2000:
            raise ValidationError("Image dimensions should not exceed 2000x2000 pixels.")






