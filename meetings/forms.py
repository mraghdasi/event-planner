from django.forms import ModelForm

from meetings.models import Room


class CreateRoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ["title"]
