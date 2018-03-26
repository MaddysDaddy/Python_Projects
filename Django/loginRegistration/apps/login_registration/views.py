# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from . models import *

from django.contrib import messages

# Create your views here.


def index(request):
    if 'user' not in request.session:
        return render(request, 'login_registration/index.html')
    else:
        return redirect('/main')


def register(request):
    if request.method == 'POST':
        errors = User.objects.user_validator(request.POST)

        if len(errors):
            for error in errors:
                messages.error(request, error)
            return redirect('/')
        else:
            user = User.objects.create_user(request.POST)
            print "Success! User created."

            new_user = User.objects.get(id=user.id)
            request.session['user'] = new_user.id

            return redirect('/main')
    else:
        return redirect('/')


def main(request):
    context = {
        'user': User.objects.get(id=request.session['user'])
    }
    return render(request, 'login_registration/main.html', context)


def login(request):
    if request.method == 'POST':
        user_login = User.objects.login(request.POST)

        if type(user_login) == User:
            request.session['user'] = user_login.id
            return redirect('/main')

        else:
            for error in user_login:
                messages.error(request, error)
            return redirect('/')

    else:
        return redirect('/')


def logout(request):
    request.session.pop('user')
    return redirect('/')
