# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

import datetime

# Create your views here.


def index(request):
    if 'words' in request.session:
        context = {'word_list': request.session['words']}
        print "context = ", context
        return render(request, 'session_words/index.html', context)
    else:
        return render(request, 'session_words/index.html')


def add_word(request):
    word_obj = {
        'created_at': datetime.datetime.now().strftime('%H:%M %p, %B %d, %Y')
    }
    for key, value in request.POST.iteritems():
        if key != 'big' or key != 'csfmiddlewaretoken':
            word_obj[key] = value
        if key == 'big':
            word_obj['big'] = 'big'

    print word_obj

    try:
        request.session['words']
    except KeyError:
        request.session['words'] = []

    word_list = request.session['words']
    word_list.append(word_obj)
    request.session['words'] = word_list

    return redirect('/')


def clear(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')
