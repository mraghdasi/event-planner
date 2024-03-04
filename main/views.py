from django.shortcuts import render

from account.models import User




def more(request):
    return render(request, 'example.html', {})


def homepage(request):
    return render(request, 'example.html', {})
