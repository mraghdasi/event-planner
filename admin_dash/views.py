from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from admin_dash.forms import EditUserForm, TeamForm, RoomForm, MeetingForm
from meetings.models import Room, Meeting
from users.models import User, Team
from utils.views.decorators import admin_required, admin_or_lead_required


@login_required(login_url='sign_in')
@admin_required
def admin_home(request):
    return render(request, 'admin_dash/home.html', {})


@login_required(login_url='sign_in')
@admin_required
def admin_users(request):
    users = User.objects.all()
    return render(request, 'admin_dash/admin_users.html', {'users': users})


@login_required(login_url='sign_in')
@admin_required
def admin_meetings(request):
    meetings = Meeting.objects.all()
    return render(request, 'admin_dash/admin_meetings.html', {'meetings': meetings})


@login_required(login_url='sign_in')
@admin_required
def admin_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'admin_dash/admin_rooms.html', {'rooms': rooms})


@login_required(login_url='sign_in')
@admin_required
def admin_teams(request):
    teams = Team.objects.all()
    return render(request, 'admin_dash/admin_teams.html', {'teams': teams})


@login_required(login_url='sign_in')
@admin_required
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
    return render(request, 'admin_dash/edit_user.html', {'form': form})


@login_required(login_url='sign_in')
@admin_required
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
    return render(request, 'admin_dash/edit_team.html', {'form': form})


@login_required(login_url='sign_in')
@admin_required
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
    return render(request, 'admin_dash/add_team.html', {'form': form})


@login_required(login_url='sign_in')
@admin_required
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
    return render(request, 'admin_dash/edit_room.html', {'form': form, 'id': pk})


@login_required(login_url='sign_in')
@admin_required
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_rooms')
        else:
            messages.error(request, 'Error updating Room. Please check the form.', 'danger')
    else:
        form = RoomForm()
    return render(request, 'admin_dash/add_room.html', {'form': form})


@login_required(login_url='sign_in')
@admin_required
def delete_room(request, pk):
    try:
        Room.objects.get(id=pk).delete()
        return JsonResponse({}, status=200)
    except Exception as e:
        return JsonResponse({'msg': 'Room Not Found!'}, status=400)


@login_required(login_url='sign_in')
@admin_or_lead_required
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
    return render(request, 'admin_dash/edit_meeting.html', {'form': form, 'id': pk})


@login_required(login_url='sign_in')
@admin_required
def delete_meeting(request, pk):
    try:
        Meeting.objects.get(id=pk).delete()
        return JsonResponse({}, status=200)
    except Exception as e:
        return JsonResponse({'msg': 'Meeting Not Found!'}, status=400)
