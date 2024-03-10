import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError

from users.forms import ProfileForm, SignUpForm, LoginForm, CustomPasswordResetForm


def generate_otp():
    o = random.randint(1000, 9999)
    return o


def send_otp(o):
    print("Your OTP is:", o)


def otp_generator(request):
    otp_generated = generate_otp()
    send_otp(otp_generated)
    request.session["otp"] = otp_generated


def phone_auth(request):
    phone_number = request.session.get('phone_number', default=None)
    if phone_number is None:
        return redirect('')
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        otp_generated = str(request.session.get('otp'))
        if otp_entered == otp_generated:
            del request.session['otp']
            user = authenticate(request, phone_number=phone_number)
            user.is_fully_authenticated = True
            user.save()
            del request.session['phone_number']
            return redirect('sign_in')
        else:
            return render(request, 'users/phone_auth.html', {'error': 'Invalid OTP'})
    else:
        otp_generator(request)
        return render(request, 'users/phone_auth.html')


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            request.session['phone_number'] = user.phone_number
            return redirect('phone_auth')
        else:
            messages.error(request, form.errors, 'danger')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username, password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                return render(request, 'users/signin.html',
                              {'form': form, 'error_message': 'Invalid username or password'})
        else:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username, password)
            messages.error(request, form.errors, 'danger')
    else:
        form = LoginForm(request)
    return render(request, 'users/signin.html', {'form': form})


def rest_password_otp(request):
    phone_number = request.session.get('phone_number', default=None)
    if phone_number is None:
        return redirect('')
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        otp_generated = str(request.session.get('otp'))
        if otp_entered == otp_generated:
            del request.session['otp']
            request.session['code_confirmed'] = True
            return redirect('reset_password')
        else:
            return render(request, 'users/reset_password_otp.html', {'error': 'Invalid OTP'})
    else:
        otp_generator(request)
        return render(request, 'users/reset_password_otp.html')


def reset_password(request):
    form = CustomPasswordResetForm()
    try:
        phone_number = request.POST['phone_number']
    except MultiValueDictKeyError:
        phone_number = None
    code_confirmed = request.session.get('code_confirmed', default=False)
    try:
        del request.session['code_confirmed']
    except KeyError:
        pass
    if request.method == 'POST' and phone_number is not None:
        user = authenticate(request, phone_number=phone_number)
        if user is not None:
            request.session['phone_number'] = phone_number
            if user.is_fully_authenticated:
                return redirect('rest_password_otp')
            else:
                return redirect('phone_auth')
        else:
            return render(request, 'users/reset_password.html', {'error': 'Your Phone Number Is Not In The Database'})
    elif request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            user = authenticate(request, phone_number=request.session.get('phone_number'))
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            del request.session['phone_number']
            return redirect('sign_in')

    return render(request, 'users/reset_password.html', {'form': form, 'code_confirmed': code_confirmed})


def sign_out(request):
    logout(request)
    return redirect('sign_in')


@login_required(login_url='sign_in')
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
