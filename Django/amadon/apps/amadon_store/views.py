# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.


def index(request):
    items = [
        {
            'item': 'Dojo Tshirt',
            'price': 19.99,
            'id': 1
        },
        {
            'item': 'Dojo Sweater',
            'price': 29.99,
            'id': 2
        },
        {
            'item': 'Dojo Cup',
            'price': 4.99,
            'id': 3
        },
        {
            'item': 'Algorithm Book',
            'price': 49.99,
            'id': 4
        },
    ]

    context = {
        'items': items
    }
    return render(request, 'amadon_store/index.html', context)


def purchase(request):
    item = int(request.POST['item'])
    quantity = int(request.POST['quantity'])
    price = 0

    if item == 1:
        price = 19.99
    if item == 2:
        price = 29.99
    if item == 3:
        price = 4.99
    if item == 4:
        price = 49.99

    total = quantity * price
    formatted_total = '${:,.2f}'.format(total)

    try:
        request.session['item_count']
        request.session['running_total']
    except KeyError:
        request.session['item_count'] = 0
        request.session['running_total'] = 0

    item_count = request.session['item_count']
    item_count += quantity
    request.session['item_count'] = item_count

    running_total = request.session['running_total']
    running_total += total
    request.session['running_total'] = running_total

    request.session['total'] = total

    print item, quantity, total

    return redirect('/confirmation')


def confirmation(request):

    context = {
        'total': '${:,.2f}'.format(request.session['total']),
        'item_count': request.session['item_count'],
        'running_total': '${:,.2f}'.format(request.session['running_total'])
    }

    return render(request, 'amadon_store/confirmation.html', context)


def home(request):
    request.session.pop('total')
    return redirect('/')
