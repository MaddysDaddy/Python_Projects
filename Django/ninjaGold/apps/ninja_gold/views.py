# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

import random
from datetime import datetime

# Create your views here.


def index(request):
    if 'total' in request.session and 'activities' in request.session:
        context = {
            'gold': request.session['total'],
            'activities': request.session['activities']
        }
        print request.session['total']
        return render(request, 'ninja_gold/index.html', context)
    else:
        print "not in session"
        return render(request, 'ninja_gold/index.html')


def process_money(request):

    gold_total = 0
    activity = {
        'time': datetime.now().strftime('%I:%M %p, %B %d, %Y')
    }

    if request.POST['place'] == 'farm':
        golds = random.randrange(10, 20)
        gold_total += golds

        activity['place'] = 'farm'
        activity['gold'] = gold_total
        activity['win'] = True

    if request.POST['place'] == 'cave':
        golds = random.randrange(5, 10)
        gold_total += golds

        activity['place'] = 'cave'
        activity['gold'] = gold_total
        activity['win'] = True

    if request.POST['place'] == 'house':
        golds = random.randrange(2, 5)
        gold_total += golds

        activity['place'] = 'house'
        activity['gold'] = gold_total
        activity['win'] = True

    if request.POST['place'] == 'casino':
        golds = random.randrange(0, 50)
        chance = random.randrange(0, 2)
        print chance

        if chance == 1:
            gold_total += golds
            activity['win'] = True

        else:
            gold_total -= golds
            activity['win'] = False

        activity['place'] = 'casino'
        activity['gold'] = gold_total

    try:
        request.session['total']
        request.session['activities']
    except KeyError:
        request.session['total'] = 0
        request.session['activities'] = []

    total = request.session['total']
    total += gold_total
    request.session['total'] = total

    activities = request.session['activities']
    activities.append(activity)
    request.session['activities'] = activities

    print request.session['total']

    return redirect('/')


def reset(request):
    if request.method == 'POST':
        for key in request.session.keys():
            del request.session[key]
        return redirect('/')
