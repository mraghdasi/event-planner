from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect

from admin_dash.forms import EditUserForm, TeamForm, RoomForm, MeetingForm
from meetings.models import Room, Meeting
from users.models import User, Team


def admin_home(request):
    return render(request, 'admin-dash/home.html', {})


def admin_users(request):
    users = User.objects.all()
    return render(request, 'admin-dash/admin_users.html', {'users': users})


def admin_meetings(request):
    meetings = Meeting.objects.all()
    return render(request, 'admin-dash/admin_meetings.html', {'meetings': meetings})


def admin_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'admin-dash/admin_rooms.html', {'rooms': rooms})


def admin_teams(request):
    teams = Team.objects.all()
    return render(request, 'admin-dash/admin_teams.html', {'teams': teams})


def edit_user(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_users')
        else:
            messages.error(request, 'Error updating User. Please check the form.', 'danger')
    else:
        form = EditUserForm(instance=user)
    return render(request, 'admin-dash/edit_user.html', {'form': form})


def edit_team(request, pk):
    team = Team.objects.get(id=pk)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('admin_teams')
        else:
            messages.error(request, 'Error updating Team. Please check the form.', 'danger')
    else:
        form = TeamForm(instance=team)
    return render(request, 'admin-dash/edit_team.html', {'form': form})


def add_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_teams')
        else:
            messages.error(request, 'Error updating Team. Please check the form.', 'danger')
    else:
        form = TeamForm()
    return render(request, 'admin-dash/add_team.html', {'form': form})


def edit_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('admin_rooms')
        else:
            messages.error(request, 'Error updating Room. Please check the form.', 'danger')
    else:
        form = RoomForm(instance=room)
    return render(request, 'admin-dash/edit_room.html', {'form': form})


def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_rooms')
        else:
            messages.error(request, 'Error updating Room. Please check the form.', 'danger')
    else:
        form = TeamForm()
    return render(request, 'admin-dash/add_room.html', {'form': form})


def edit_meeting(request, pk):
    meeting = Meeting.objects.get(id=pk)
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            return redirect('admin_meetings')
        else:
            messages.error(request, 'Error updating Meeting. Please check the form.', 'danger')
    else:
        form = MeetingForm(instance=meeting)
    return render(request, 'admin-dash/edit_meeting.html', {'form': form})


def delete_meeting(request, pk):
    try:
        Meeting.objects.get(id=pk).delete()
        return JsonResponse({}, status=200)
    except Exception as e:
        return JsonResponse({'msg': 'Meeting Not Found!'}, status=400)
