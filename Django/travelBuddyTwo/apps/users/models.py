# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


import bcrypt

from django.core.exceptions import ObjectDoesNotExist

# Create your models here.


class UserManager(models.Manager):
    def user_validator(self, postData):

        errors = []
        if len(User.objects.filter(username=postData['username'])):
            errors.append(
                'Your email address has already been registered. Please log in.')
        else:
            if len(postData['name']) < 3:
                errors.append('Name must be at least 2 characters long.')
            if len(postData['username']) < 3:
                errors.append('Username must be at least 2 characters long.')
            if len(postData['password']) < 8:
                errors.append('Password must be at least 8 characters long.')
            if postData['password'] != postData['confirm_password']:
                errors.append('Passwords do not match')

        return errors

    def create_user(self, postData):
        print postData
        pwhash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())

        user = User.objects.create(
            name=postData['name'],
            username=postData['username'],
            pwhash=pwhash
        )

        return user

    def login(self, postData):
        username = postData['username']
        password = postData['password']
        errors = []

        try:
            user = User.objects.get(username=username)

            if bcrypt.checkpw(password.encode(), user.pwhash.encode()):
                return user
            else:
                errors.append('Incorrect login info.')
                print "incorrect login info"
                return errors
        except ObjectDoesNotExist:
            print "User not found."
            errors.append('User not found. Please register below.')
            return errors


class User(models.Model):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)

    pwhash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
