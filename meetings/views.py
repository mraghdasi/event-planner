import json
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import View

from meetings.forms import MeetingForm, CommentRoomForm
from meetings.models import Room, Meeting


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


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

    @staticmethod
    def get_room(room_id: int):
        room = Room.objects.filter(id=room_id).annotate(meeting_count=Count('meetings'))

        if not room.exists():
            room = None
            comments = None
        else:
            room = room[0]
            comments = room.comments.all()

        return room, comments

    def get(self, request, id):
        room, comments = self.get_room(id)

        return render(request, 'meeting/room_detail.html',
                      {'comments': comments, 'room': room, 'user': request.user, 'form': self.form_class,
                       'meetings': json.dumps(self.get_room_meetings(id), cls=CustomJSONEncoder)})

    def post(self, request, id, *args, **kwargs):
        forms = self.form_class(request.POST)
        room, comments = self.get_room(id)

        has_error = True
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.room = forms.cleaned_data.get('room')
            has_error = False
            form.save()

            context = {'comments': comments, 'room': room, 'user': request.user, 'form': self.form_class,
                       'meetings': json.dumps(self.get_room_meetings(id),
                                              cls=CustomJSONEncoder), 'has_error': has_error}
            return render(request, 'meeting/room_detail.html', context)
        else:
            context = {'comments': comments, 'room': room, 'user': request.user, 'form': forms,
                       'meetings': json.dumps(self.get_room_meetings(id),
                                              cls=CustomJSONEncoder), 'has_error': has_error}
            return render(request, 'meeting/room_detail.html', context)


@login_required(login_url='sign_in')
def create_comment(request, pk):
    user = request.user
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        form = CommentRoomForm(request.POST, user=user, room=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment Created Successfully!', 'success')
            return redirect('profile')
        else:
            messages.error(request, 'Error Creating User. Please check the form.', 'danger')
    else:
        form = CommentRoomForm(user=user, room=room)
    return render(request, 'meeting/add_comment.html', {'form': form, })


@login_required(login_url='sign_in')
def room_comments(request, pk):
    room = Room.objects.get(id=pk)
    comments = room.comments.all()
    return render(request, 'meeting/room_comments.html', {'comments': comments, 'room': room})
