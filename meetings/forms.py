from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from meetings.models import Meeting, CommentRoom
from users.models import Team


class MeetingForm(ModelForm):
    team = forms.ModelChoiceField(queryset=Team.objects.filter(is_active=True),
                                  widget=forms.Select(attrs={'class': 'tw-w-full'}))

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
                raise forms.ValidationError(
                    "The selected time range overlaps with an existing meeting for the chosen room.")

        return cleaned_data


class CommentRoomForm(forms.ModelForm):
    class Meta:
        model = CommentRoom
        fields = ['body', 'rate']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.room = kwargs.pop('room', None)
        super(CommentRoomForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == 'rate':
                field.widget.attrs.update({'max': 5})
                field.widget.attrs.update({'min': 0})
            field.widget.attrs.update({'class': 'form-control mb-3'})

    def save(self, commit=True):
        instance = super(CommentRoomForm, self).save(commit=False)
        if self.user:
            instance.user = self.user
        if self.room:
            instance.room = self.room
        if commit:
            instance.save()
        return instance
