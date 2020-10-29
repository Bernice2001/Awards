from django.contrib.auth import login, authenticate
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.http  import HttpResponse
import datetime as dt
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.urls import reverse
from django.db import transaction
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
# from .serializer import *
from rest_framework import status

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.job_title = form.cleaned_data.get('job_title')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def signin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(request,'/')
    
    return render(request, '/django_registration/login.html')

@login_required
def logout(request):
    django_logout(request)
    return  HttpResponseRedirect('/')