from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError

from meetings.models import Meeting, Room
from users.models import Team


class MeetingForm(ModelForm):
    team = forms.ModelChoiceField(queryset=Team.objects.filter(is_active=True), widget=forms.Select(attrs={'class': 'tw-w-full'}))

    class Meta:
        model = Meeting
        fields = ('title', 'team', 'room', 'start_date', 'end_date')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'tw-w-full'}),
            'team': forms.Select(attrs={'class': 'tw-w-full'}),
            'room': forms.HiddenInput(),
            'start_date': forms.DateInput(
                format=('%d/%m/%Y %H:%M'),
                attrs={'class': 'tw-w-full',
                       'placeholder': 'Select a date',
                       'type': 'datetime-local'}),
            'end_date': forms.DateInput(
                format=('%d/%m/%Y %H:%M'),
                attrs={'class': 'tw-w-full',
                       'placeholder': 'Select a date',
                       'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        room = cleaned_data.get('room')

        if start_date and end_date and start_date >= end_date:
            raise ValidationError("End date must be later than start date")

        if start_date and end_date and room:
            overlapping_meetings = Meeting.objects.filter(
                room=room,
                start_date__lt=end_date,
                end_date__gt=start_date
            )

            if overlapping_meetings.exists():
                raise forms.ValidationError("The selected time range overlaps with an existing meeting for the chosen room.")

        return cleaned_data
