import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.forms import ModelForm

from .models import User


class SignUpForm(UserCreationForm):
    password_confirm = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password', 'image']

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 5:
            raise forms.ValidationError("Username must be at least 5 characters long.")
        if username.isdigit():
            raise forms.ValidationError("Username cannot consist of only numbers.")
        if not username.isascii():
            raise forms.ValidationError("Username must contain English characters only.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Please enter a valid email address.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not re.match(r"^(09)([0-9]{9})$", phone_number):
            raise forms.ValidationError("Enter a valid phone number.")
        return phone_number

    def clean_password(self):
        password = self.cleaned_data['password']
        if not re.match(r"^.{5,255}$", password):
            raise forms.ValidationError("Password should be at least 5 characters long.")
        if not re.search(r"(.*[!@#$%^&*()_+\-=\[\]{};':\"\\,.<>?].*){1,}", password):
            raise forms.ValidationError("Password should have at least one special character.")
        if not re.search(r"(.*[A-Z].*){1,}", password):
            raise forms.ValidationError("Password should have at least one uppercase letter")
        if not re.search(r"(.*\d.*){2,}", password):
            raise forms.ValidationError("Password should have at least two digits")
        return password

    def clean_password_confirm(self):
        password_confirm = self.cleaned_data['password_confirm']
        password = self.cleaned_data.get('password')
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        return password_confirm

    def clean_image(self):
        image = self.cleaned_data['image']
        if image:
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Image must be in JPG or JPEG or PNG format.")
        return image


class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget.attrs.update({'class': 'dropify'})
            else:
                field.widget.attrs.update({'class': 'form-control mb-3'})

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'image']
