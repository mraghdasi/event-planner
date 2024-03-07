import random

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from users.forms import ProfileForm, SignUpForm


def generate_otp():
    o = random.randint(1000, 9999)
    return o


def send_otp(o):
    print("Your OTP is:", o)


def otp(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        otp_generated = request.session.get('otp')

        if otp_entered == otp_generated:
            form_data = request.session.get('form_data')
            form = SignUpForm(form_data)
            form.save()
            user = authenticate(request, username=request.session.get('username'),
                                password=request.session.get('password'))
            del request.session['otp']
            del request.session['username']
            del request.session['password']
            del request.session['form_data']
            if user is not None:
                login(request, user)
                return redirect('homepage')
        else:
            return render(request, 'users/otp.html', {'error': 'Invalid OTP'})
    else:
        return render(request, 'users/otp.html')


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            otp_generated = generate_otp()

            request.session['otp'] = otp_generated
            request.session['username'] = form.cleaned_data.get('username')
            request.session['password'] = form.cleaned_data.get('password')
            request.session['form_data'] = {i: form.cleaned_data[i] for i in form.cleaned_data if i != 'image'}
            send_otp(otp_generated)
            return redirect('otp')
        else:
            messages.error(request, form.errors, 'danger')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        ...
    else:
        return render(request, 'users/login.html', {})


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User Updated Successfully!', 'success')
            return redirect('profile')
        else:
            messages.error(request, 'Error updating User. Please check the form.', 'danger')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})
