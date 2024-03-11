import json
from datetime import datetime

from django.shortcuts import render, redirect
from django.core.serializers.json import DjangoJSONEncoder
from django.views import View
from django.db.models import Count
from django.contrib import messages

from meetings.forms import MeetingForm
from meetings.models import Room, Meeting


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def more(request):
    return render(request, 'meeting/../templates/example.html', {})


def homepage(request):
    return render(request, 'meeting/../templates/example.html', {})


class RoomList(View):
    def get(self, request):
        rooms = Room.objects.annotate(meeting_count=Count('meetings'))
        return render(request, 'meeting/room_list.html', {'rooms': rooms})


class RoomDetail(View):
    form_class = MeetingForm

    @staticmethod
    def get_room_meetings(room_id: int):
        meetings = Meeting.objects.filter(room_id=room_id)
        meetings = list(meetings.values('title', 'id', 'start_date', 'end_date'))

        for meeting in meetings:
            meeting['start'] = meeting.pop('start_date')
            meeting['end'] = meeting.pop('end_date')
            meeting['className'] = 'info'
            meeting['allDay'] = False

        return meetings

    def get(self, request, id):
        room = Room.objects.filter(id=id).annotate(meeting_count=Count('meetings'))

        if not room.exists():
            room = None
        else:
            room = room[0]

        return render(request, 'meeting/room_detail.html',
                      {'room': room, 'user': request.user, 'form': self.form_class,
                       'meetings': json.dumps(self.get_room_meetings(id), cls=CustomJSONEncoder)})

    def post(self, request, *args, **kwargs):

        forms = self.form_class(request.POST)

        has_error = True
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.room = forms.cleaned_data.get('room')
            has_error = False
            form.save()

            context = {'room': forms.cleaned_data.get('room'), 'user': request.user, 'form': self.form_class,
                       'meetings': json.dumps(self.get_room_meetings(forms.cleaned_data.get('room')),
                                              cls=CustomJSONEncoder), 'has_error': has_error}
            return render(request, 'meeting/room_detail.html', context)
        else:
            for error in forms.errors:
                messages.error(request, error)
            context = {'room': forms.cleaned_data.get('room'), 'user': request.user, 'form': forms,
                       'meetings': json.dumps(self.get_room_meetings(forms.cleaned_data.get('room')),
                                              cls=CustomJSONEncoder), 'has_error': has_error}
            return render(request, 'meeting/room_detail.html', context)
