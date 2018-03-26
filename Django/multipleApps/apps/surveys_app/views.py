# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse

# Create your views here.


def surveys(response):
    return HttpResponse('placeholder to display all the surveys created.')


def new(response):
    return HttpResponse('placeholder for users to add a new survey.')
