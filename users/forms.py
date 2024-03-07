from django.forms import ModelForm

from users.models import User


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
