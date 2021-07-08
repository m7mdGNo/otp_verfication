from django.shortcuts import render,redirect
from . models import Profile
import random
from django.contrib.auth.forms import User,UserCreationForm
from django.contrib import messages
from django.contrib.auth import login,authenticate
from django.core.mail import EmailMessage,send_mail


def home(request):
    return render(request,'home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is taken.')
                return redirect('register')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                return redirect('register')
            user_obj = User( username = username , email = email )
            user_obj.set_password(password)
            user_obj.save()
            otp = str(random.randint(1111,9999))
            profile_obj = Profile.objects.create(user=user_obj,otp=otp,username=username,email=email)
            profile_obj.save()
            send_message(profile_obj)
            return redirect('otp')
        except Exception as e:
            print(e)
    return render(request,'register.html')


def otp(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        print(otp)
        profile_obj = Profile.objects.filter(otp=otp).first()

        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'successfull')
        else:
            messages.success(request, 'error')
        if profile_obj.is_verified == True:
            messages.success(request, 'you have verified your acc')

    return render(request,'otp.html')


def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')

        profile_obj = Profile.objects.filter(user=user_obj).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/accounts/login')

        else:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


def send_message( profile):
    otp = profile.otp
    email = profile.user.email
    email = EmailMessage('hi', f'verfication code is {otp}', to=[email])
    email.send()




