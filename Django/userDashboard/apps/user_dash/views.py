# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from . models import *

from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, 'user_dash/index.html')


def login(request):
    return render(request, 'user_dash/login.html')


def user_login(request):
    if request.method == 'POST':
        user_login = User.objects.login(request.POST)

        if type(user_login) == User:
            request.session['user'] = user_login.id

            if user_login.user_level == 9:
                request.session['admin'] = True
            else:
                request.session['admin'] = False

            return redirect('/dashboard')

        else:
            for error in user_login:
                messages.error(request, error)
            return redirect('/login')

    else:
        return redirect('/login')


def create(request):
    if request.method == 'POST':
        errors = User.objects.user_validator(request.POST)

        if len(errors):
            for error in errors:
                messages.error(request, error)
            return redirect('/register')
        else:
            user = User.objects.create_user(request.POST)

            new_user = User.objects.get(id=user.id)
            request.session['user'] = new_user.id

            return redirect('/dashboard')
    return redirect('/register')


def dashboard(request):
    user = User.objects.get(id=request.session['user'])

    if 'user' in request.session:
        logged_in = True
    else:
        logged_in = False

    # def is_admin(user):

        # else:
        #     admin = False

        # return admin

    context = {
        'user': User.objects.get(id=request.session['user']),
        'all_users': User.objects.all(),
        'admin': request.session['admin'],
        'logged': logged_in
    }
    return render(request, 'user_dash/dashboard.html', context)


def profile(request, user_id):
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'user_dash/profile.html', context)


def profile_update(request, user_id):
    user = User.objects.update_user(request.POST, user_id)

    if type(user) == User:
        return redirect('/' + user_id + '/profile')
    else:
        for error in user:
            messages.error(request, error)
        return redirect('/' + user_id + '/profile')


def user_details(request, user_id):
    context = {
        'user': User.objects.get(id=user_id),
        'posts': Post.objects.filter(user__id=user_id),
        'comments': Comment.objects.all()
    }
    print context['user'].first_name
    return render(request, 'user_dash/show.html', context)


def message(request, user_id):
    if request.method == 'POST':
        errors = Post.objects.validate_post(request.POST)

        if len(errors):
            for error in errors:
                messages.error(request, error)
            return redirect('/users/show/' + user_id)

        else:
            post_user_id = request.session['user']
            Post.objects.create_post(
                request.POST, user_id, post_user_id)
            return redirect('/users/show/' + user_id)


def comment(request, user_id, post_id):
    if request.method == 'POST':
        errors = Comment.objects.validate_comment(request.POST)

        if len(errors):
            for error in errors:
                messages.error(request, error)
            return redirect('/users/show' + user_id)

        else:
            post = Post.objects.get(id=post_id)

            from_user = request.session['user']
            print from_user, post_id, request.POST['comment']
            Comment.objects.create_comment(request.POST, from_user, post_id)
            return redirect('/users/show/' + user_id)


def register(request):
    return render(request, 'user_dash/register.html')


def logout(request):
    request.session.pop('user')
    return redirect('/')
