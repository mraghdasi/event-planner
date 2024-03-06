from django.shortcuts import render
from django.views import View
from django.db.models import Count

from meetings.models import Room


class RoomList(View):
    def get(self, request):
        rooms = Room.objects.annotate(meeting_count=Count('meetings'))
        return render(request, 'meeting/room_list.html', {'rooms': rooms})


class RoomDetail(View):
    def get(self, request, id):
        room = Room.objects.filter(id=id).annotate(meeting_count=Count('meetings'))

        if not room.exists():
            room = None
        else:
            room = room[0]
        return render(request, 'meeting/room_detail.html', {'room': room})
