from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from meetings.forms import CreateRoomForm
from users.models import User


def more(request):
    return render(request, 'home_templates/example.html', {})


def homepage(request):
    return render(request, 'home_templates/example.html', {})


class CreateRoomView(CreateView):
    template_name = 'meetings/create_room.html'
    form_class = CreateRoomForm
    success_url = reverse_lazy('index')
