from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render


def sign_up(request):
    return render(request, 'users/signup.html', {})


@login_required
def profile(request):
    return render(request, 'users/profile.html', {})


@login_required
def edit_profile_api(request):
    try:
        username = request.POST['username']
    except Exception as e:
        msg = 'Username Value Not Sent'
        return JsonResponse({'msg': msg}, status=400)
    try:
        first_name = request.POST['first_name']
    except Exception as e:
        msg = 'First Name Value Not Sent'
        return JsonResponse({'msg': msg}, status=400)
    try:
        last_name = request.POST['last_name']
    except Exception as e:
        msg = 'Last Name Value Not Sent'
        return JsonResponse({'msg': msg}, status=400)
    try:
        email = request.POST['email']
    except Exception as e:
        msg = 'Email Value Not Sent'
        return JsonResponse({'msg': msg}, status=400)
    try:
        phone_number = request.POST['phone_number']
    except Exception as e:
        msg = 'Phone Number Value Not Sent'
        return JsonResponse({'msg': msg}, status=400)

    try:
        image = request.FILES['image']
    except Exception as e:
        image = None

    request.user.username = username
    request.user.first_name = first_name
    request.user.last_name = last_name
    request.user.email = email
    request.user.phone_number = phone_number
    if image:
        request.user.image = image

    request.user.save()
    return JsonResponse({}, status=200)
