from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'image']

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
        # You can add more complex email validation if needed
        return email

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        # Add your password validation logic here
        return password1

    def clean_image(self):
        image = self.cleaned_data['image']
        if image:
            # Validate image file format
            if not image.name.lower().endswith(('.jpg', '.jpeg')):
                raise forms.ValidationError("Image must be in JPG or JPEG format.")
        return image
