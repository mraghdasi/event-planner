from django.shortcuts import render


def admin_home(request):
    return render(request, 'admin-dash/home.html', {})
def admin_users(request):
    return render(request, 'admin-dash/admin_users.html', {})
def admin_meetings(request):
    return render(request, 'admin-dash/admin_meetings.html', {})
def admin_rooms(request):
    return render(request, 'admin-dash/admin_rooms.html', {})
def admin_teams(request):
    return render(request, 'admin-dash/admin_teams.html', {})

# Create your views here.
