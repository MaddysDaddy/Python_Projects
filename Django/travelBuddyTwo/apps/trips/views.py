# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponseRedirect, reverse

from ..users.models import *

from . models import *

from django.contrib import messages
# Create your views here.


def main(request):
    if 'user' in request.session:
        current_user = User.objects.get(id=request.session['user'])

        context = {
            'user': current_user,
            'user_trips': Trip.objects.filter(travelers__id=request.session['user']),
            'all_trips': Trip.objects.all()
        }
        return render(request, 'trips/main.html', context)

    else:
        return redirect(reverse('login:index'))

# navigate to add trip page


def addplan(request):
    if 'user' in request.session:
        current_user = User.objects.get(id=request.session['user'])

        return render(request, 'trips/addplan.html')
    else:
        return redirect('/')

# Add a trip to the database


def addtrip(request):
    if request.method == 'POST':
        current_user = User.objects.get(id=request.session['user'])

        errors = Trip.objects.trip_validator(request.POST)

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('trips:addplan')

        else:
            trip = Trip.objects.create_trip(request.POST, current_user)
            return redirect('trips:main')

    else:
        return redirect('trips:addplan')


def destination(request, trip_id):
    if 'user' in request.session:
        current_user = User.objects.get(id=request.session['user'])
        trip = Trip.objects.get(id=trip_id)

        context = {
            'trip': Trip.objects.get(id=trip_id),
            'joined_users': User.objects.filter(trips__id=trip_id).exclude(id=trip.planner.id)
        }
    return render(request, 'trips/destination.html', context)


def join(request, trip_id):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['user'])

        errors = Trip.objects.join_validator(trip_id, user)
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('trips:main')
        else:
            join_user = Trip.objects.join(trip_id, user)
            return redirect('trips:main')

    else:
        return redirect('trips:main')
