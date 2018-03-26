# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.core.exceptions import ObjectDoesNotExist

import re
import bcrypt

# Create your models here.


class UserManager(models.Manager):
    def create_user(self, postData):
        pwhash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        print pwhash
        user = User.objects.create(
            first_name=postData['first_name'],
            last_name=postData['last_name'],
            email=postData['email'],
            pwhash=pwhash
        )
        return user

    def user_validator(self, postData):
        EMAIL_REGEX = re.compile(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

        errors = []
        if len(User.objects.filter(email=postData['email'])):
            errors.append(
                'Your email address has already been registered. Please log in.')
        else:
            if len(postData['first_name']) < 2:
                errors.append('First name must be at least 2 characters long.')
            if len(postData['last_name']) < 2:
                errors.append('Last name must be at least 2 characters long.')
            if not EMAIL_REGEX.match(postData['email']):
                errors.append('Please enter a valid email address.')
            if len(postData['password']) < 8:
                errors.append('Password must be at least 8 characters long.')
            if postData['password'] != postData['confirm-password']:
                errors.append('Passwords do not match')

        return errors

    def login(self, postData):
        email = postData['username']
        password = postData['password']
        errors = []

        try:
            user = User.objects.get(email=email)

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
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=255)
    pwhash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
