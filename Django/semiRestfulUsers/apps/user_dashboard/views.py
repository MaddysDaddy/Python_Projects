# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse

from django.contrib import messages

from . models import *

# Create your views here.


def index(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'user_dashboard/index.html', context)


def new(request):

    return render(request, 'user_dashboard/new.html')


def create(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, error)
    else:
        user = User.objects.create()
        user.first_name = request.POST['fname']
        user.last_name = request.POST['lname']
        user.email = request.POST['email']
        user.save()

    return redirect('/new')


def show(request, user_id):
    user = User.objects.get(id=user_id)

    context = {
        'user': user
    }
    return render(request, 'user_dashboard/show.html', context)


def edit(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        'user': user
    }

    return render(request, 'user_dashboard/edit.html', context)


def update(request, user_id):
    user = User.objects.get(id=user_id)

    errors = User.objects.user_validator(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, error)
    else:
        user.first_name = request.POST['fname']
        user.last_name = request.POST['lname']
        user.email = request.POST['email']
        user.save()
    return redirect('/' + user_id + '/edit')


def delete(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('/')
