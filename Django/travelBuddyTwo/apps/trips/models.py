# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from ..users.models import User

from datetime import datetime

# Create your models here.


class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = []
        today = datetime.now()
        fromdate = datetime.strptime(postData['from_date'], '%Y-%m-%d')
        enddate = datetime.strptime(postData['end_date'], '%Y-%m-%d')

        if len(postData['destination']) < 1:
            errors.append("Destination can't be blank.")
        if fromdate < today:
            errors.append("Cannot travel in the past.")
        if enddate < fromdate:
            errors.append("You can't travel to the past fool!")

        return errors

    def create_trip(self, postData, current_user):
        fromdate = datetime.strptime(postData['from_date'], '%Y-%m-%d')
        enddate = datetime.strptime(postData['end_date'], '%Y-%m-%d')

        trip = Trip.objects.create(
            planner=current_user,
            destination=postData['destination'],
            description=postData['description'],
            from_date=fromdate,
            end_date=enddate
        )

        trip.travelers.add(current_user)
        trip.save()

        return trip

    def join_validator(self, trip_id, user):
        errors = []

        if len(Trip.objects.filter(id=trip_id, travelers__id=user.id)):
            print Trip.objects.filter(travelers__id=user.id)
            errors.append('You are already part of this trip.')

        return errors

    def join(self, trip_id, user):
        trip = Trip.objects.get(id=trip_id)

        trip.travelers.add(user)
        trip.save()
        return trip


class Trip(models.Model):
    planner = models.ForeignKey(User, related_name="trip_planner")
    destination = models.CharField(max_length=255)
    description = models.TextField()
    from_date = models.DateTimeField()
    end_date = models.DateTimeField()
    travelers = models.ManyToManyField(User, related_name='trips')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripManager()
