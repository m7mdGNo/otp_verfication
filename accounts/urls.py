from django.contrib import admin
from django.urls import path, include
from .views import home,register,otp,Login

urlpatterns = [
    path('',home,name='home' ),
    path('register',register,name='register'),
    path('verfication',otp,name='otp'),
    path('login',Login,name='login'),


]