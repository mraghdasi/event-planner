from django.shortcuts import render


def more(request):
    return render(request, 'meeting/example.html', {})


def homepage(request):
    return render(request, 'meeting/example.html', {})
