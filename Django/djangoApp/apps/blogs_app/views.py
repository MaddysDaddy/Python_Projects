# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse

# Create your views here.


def index(request):
    response = "Placeholder for list of blogs"
    return HttpResponse(response)


def new(request):
    response = "Placeholder to display a new form to create a new blog."
    return HttpResponse(response)


def create(request):
    return redirect('/')


def show(request, id):
    return HttpResponse('Placeholder for blog number {0}.'.format(id))


def edit(request, id):
    return HttpResponse('Placeholder to edit blog number {0}.'.format(id))


def destroy(request, id):
    return redirect('/')
