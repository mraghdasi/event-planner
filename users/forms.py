import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.forms import ModelForm

from .models import User
from secrets import compare_digest


class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs['placeholder'] = '5 Characters long can\'t be all nums Eng only'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Eng only'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Eng only'
        self.fields['email'].widget.attrs['placeholder'] = 'example@example.com'
        self.fields['phone_number'].widget.attrs['placeholder'] = '09121231234'
        self.fields['password1'].widget.attrs[
            'placeholder'] = '8 Characters long at least 1 special character'
        self.fields['password2'].widget.attrs[
            'placeholder'] = 'and 1 uppercase letter and 2 digits'

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2',
                  'image']

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 5:
            raise forms.ValidationError("Username must be at least 5 characters long.")
        if username.isdigit():
            raise forms.ValidationError("Username cannot consist of only numbers.")
        if not username.isascii():
            raise forms.ValidationError("Username must contain English characters only.")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise forms.ValidationError("Your first name must contain only letters.")
        if not first_name.isascii():
            raise forms.ValidationError("Your first name must be in English.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise forms.ValidationError("Your last name must contain only letters.")
        if not last_name.isascii():
            raise forms.ValidationError("Your last name must be in English.")
        return last_name

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
        password = self.cleaned_data['password1']
        if not re.match(r"^.{8,255}$", password):
            raise forms.ValidationError("Password should be at least 8 characters long.")
        if not re.search(r"(.*[!@#$%^&*()_+\-=\[\]{};':\"\\,.<>?].*)+", password):
            raise forms.ValidationError("Password should have at least one special character.")
        if not re.search(r"(.*[A-Z].*)+", password):
            raise forms.ValidationError("Password should have at least one uppercase letter")
        if not re.search(r"(.*\d.*){2,}", password):
            raise forms.ValidationError("Password should have at least two digits")
        return password

    def clean_password_confirm(self):
        password_confirm = self.cleaned_data['password2']
        password = self.cleaned_data['password']
        if not compare_digest(password, password_confirm):
            raise forms.ValidationError("Passwords do not match")
        return password_confirm

    def clean_image(self):
        image = self.cleaned_data['image']
        if image:
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Image must be in JPG or JPEG or PNG format.")
        return image


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class CustomPasswordResetForm(forms.Form):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    def clean_password(self):
        password = self.cleaned_data['new_password1']
        if not re.match(r"^.{8,255}$", password):
            raise forms.ValidationError("Password should be at least 8 characters long.")
        if not re.search(r"(.*[!@#$%^&*()_+\-=\[\]{};':\"\\,.<>?].*)+", password):
            raise forms.ValidationError("Password should have at least one special character.")
        if not re.search(r"(.*[A-Z].*)+", password):
            raise forms.ValidationError("Password should have at least one uppercase letter")
        if not re.search(r"(.*\d.*){2,}", password):
            raise forms.ValidationError("Password should have at least two digits")
        return password

    def clean_password_confirm(self):
        password_confirm = self.cleaned_data['new_password2']
        password = self.cleaned_data['new_password1']
        if not compare_digest(password, password_confirm):
            raise forms.ValidationError("Passwords do not match")
        return password_confirm


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
