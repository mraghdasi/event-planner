from django.forms import ModelForm

from meetings.models import Room, Meeting
from users.models import User, Team


class EditUserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget.attrs.update({'class': 'dropify'})
            elif field_name == 'is_lead':
                pass
            else:
                field.widget.attrs.update({'class': 'form-control mb-3'})

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'image', 'is_lead', 'team']


class TeamForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs.update({'class': 'form-control mb-3'})

    class Meta:
        model = Team
        fields = ['title', 'is_active']


class RoomForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs.update({'class': 'form-control mb-3'})

    class Meta:
        model = Room
        fields = ['title', 'is_active']


class MeetingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MeetingForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if 'date' in field_name:
                field.widget.attrs.update({'class': 'form-control mb-3 date_picker_custom'})
            else:
                field.widget.attrs.update({'class': 'form-control mb-3'})

    class Meta:
        model = Meeting
        fields = ['title', 'team', 'room', 'start_date', 'end_date']
