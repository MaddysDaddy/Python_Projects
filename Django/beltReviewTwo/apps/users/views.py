# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse, HttpResponseRedirect

from . models import *

from django.contrib import messages
# Create your views here.


def index(request):
    if 'user' not in request.session:
        return render(request, 'users/welcome.html')
    else:
        return HttpResponseRedirect(reverse('reviews:index'))


def login(request):
    if request.method == 'POST':
        user = User.objects.login(request.POST)

        if type(user) == User:
            request.session['user'] = user.id
            return HttpResponseRedirect(reverse('reviews:index'))
        else:
            for error in user:
                messages.error(request, error)
            return redirect('/')

    else:
        return redirect('/')


def register(request):
    if request.method == 'POST':
        errors = User.objects.user_validator(request.POST)

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('/')

        else:
            user = User.objects.create_user(request.POST)

            new_user = User.objects.get(id=user.id)
            request.session['user'] = new_user.id

            return HttpResponseRedirect(reverse('reviews:index'))
    else:
        return redirect('/')


def logout(request):
    request.session.pop('user')
    return redirect('/')
