# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse

# Create your views here.


def register(request):
    return HttpResponse('placeholder for users to create new user record.')


def login(request):
    print "login"
    return HttpResponse('placeholder for users to login.')


def new(request):
    return HttpResponse('placeholder for new user')


def users(request):
    print "users"
    return HttpResponse('placeholder to later display all the list of users')
