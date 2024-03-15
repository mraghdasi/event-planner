from django.forms import ModelForm
from django import forms
from django.utils import timezone

from meetings.models import Room, Meeting
from users.models import User, Team


class EditUserForm(ModelForm):
    team = forms.ModelChoiceField(queryset=Team.objects.filter(is_active=True),
                                  widget=forms.Select(attrs={'class': 'tw-w-full'}), required=False)

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

    def clean(self):
        try:
            if self.cleaned_data['is_lead'] and not self.cleaned_data['team']:
                raise forms.ValidationError('A Lead must have a team')
        except KeyError:
            raise forms.ValidationError('Team Not Found')


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
        fields = ['title', 'is_active', 'description', 'capacity']


class MeetingForm(ModelForm):
    team = forms.ModelChoiceField(queryset=Team.objects.filter(is_active=True),
                                  widget=forms.Select(attrs={'class': 'tw-w-full'}))
    room = forms.ModelChoiceField(queryset=Room.objects.filter(is_active=True),
                                  widget=forms.Select(attrs={'class': 'tw-w-full'}))

    def __init__(self, *args, **kwargs):
        super(MeetingForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if 'date' in field_name:
                field.widget.attrs.update({'class': 'form-control mb-3 date_picker_custom'})
            else:
                field.widget.attrs.update({'class': 'form-control mb-3'})

    class Meta:
        model = Meeting
        fields = ('title', 'team', 'room', 'start_date', 'end_date')

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        room = cleaned_data.get('room')
        team = cleaned_data.get('team')

        try:
            room = Room.objects.get(title=room)
        except Room.DoesNotExist:
            raise forms.ValidationError('Room does not exist')

        try:
            team = Team.objects.get(title=team)
        except Team.DoesNotExist:
            raise forms.ValidationError('Team does not exist')

        if team.get_population() > room.capacity:
            raise forms.ValidationError('This team has more members than the room capacity.')

        if start_date >= end_date:
            raise forms.ValidationError("End date must be later than start date")

        if start_date < timezone.now() or end_date < timezone.now():
            raise forms.ValidationError("You can't set a date that is passed (timezone : UTC)")

        if start_date and end_date and room:
            overlapping_meetings = Meeting.objects.filter(
                room=room,
                start_date__lt=end_date,
                end_date__gt=start_date
            )

            if overlapping_meetings.exists():
                raise forms.ValidationError(
                    "The selected time range overlaps with an existing meeting for the chosen room.")

        return cleaned_data
