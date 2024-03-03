from django.shortcuts import render

from account.models import Profile


def master(request):
    try:
        p = Profile.objects.get(username=request.user.username)
        return {'profile': p}
    except Exception as e:
        return {}


def more(request):
    return render(request, 'example.html', {})


def homepage(request):
    return render(request, 'example.html', {})
