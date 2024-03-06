from django.shortcuts import render


def more(request):
    return render(request, 'meeting/../templates/example.html', {})


def homepage(request):
    return render(request, 'meeting/../templates/example.html', {})
