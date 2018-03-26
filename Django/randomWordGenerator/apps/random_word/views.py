# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from django.utils.crypto import get_random_string

# Create your views here.


def index(request):
    if 'random_word' not in request.session:
        return render(request, 'random_word/index.html')
    else:
        context = {
            'word': request.session['random_word']
        }
        return render(request, 'random_word/index.html', context)


def random(request):
    if request.method == 'POST':
        random_word = get_random_string(length=16).upper()
        request.session['random_word'] = random_word
        return redirect('/')
    else:
        return redirect('/')
