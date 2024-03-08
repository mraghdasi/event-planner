import random

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

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


@login_required(login_url='/users/login/')
def phone_auth(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        otp_generated = str(request.session.get('otp'))
        if otp_entered == otp_generated:
            del request.session['otp']
            user = request.user
            user.is_fully_authenticated = True
            user.save()
            return redirect('profile')
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
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
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
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page or profile page
                return redirect('/users/profile/')
            else:
                # Authentication failed, handle accordingly
                return render(request, 'users/signin.html',
                              {'form': form, 'error_message': 'Invalid username or password'})
    else:
        form = LoginForm()
    return render(request, 'users/signin.html', {'form': form})


def rest_password_otp(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        otp_generated = str(request.session.get('otp'))
        if otp_entered == otp_generated:
            del request.session['otp']
            user = authenticate(request, phone_number=request.session.get('phone_number'))
            login(request, user)
            del request.session['phone_number']
            return redirect('reset_password')
        else:
            return render(request, 'users/phone_auth.html', {'error': 'Invalid OTP'})
    else:
        otp_generator(request)
        return render(request, 'users/reset_password_otp.html')


def reset_password(request):
    form = CustomPasswordResetForm()
    if request.method == 'POST' and request.POST['phone_number'] is not None:
        phone_number = request.POST['phone_number']
        user = authenticate(request, phone_number=phone_number)
        if user is not None:
            if user.is_fully_authenticated:
                request.session['phone_number'] = phone_number
                return redirect('rest_password_otp')
            else:
                return redirect('phone_auth')
        else:
            return render(request, 'users/reset_password.html', {'error': 'Your Phone Number Is Not In The Database'})
    elif request.method == 'POST':
        ...
    return render(request, 'users/reset_password.html', {'form': form})


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
