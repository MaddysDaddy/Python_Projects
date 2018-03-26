# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.


def index(request):
    return render(request, 'surveys/index.html')


def process(request):
    if 'count' in request.session:
        request.session['count'] += 1
    else:
        request.session['count'] = 0
    #request.session['count'] += 1
    request.session['context'] = {
        'name': request.POST['name'],
        'dojo': request.POST['dojo'],
        'language': request.POST['language'],
        'comment': request.POST['comment'],
        'count': request.session['count']
    }

    return redirect('/result')


def result(request):
    print request.session['count'], "- in request"
    context = request.session['context']

    return render(request, 'surveys/success.html', context)
