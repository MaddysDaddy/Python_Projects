# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import re

# Create your models here.


class UserManager(models.Manager):
    def user_validator(self, postData):

        errors = []
        EMAIL_REGEX = re.compile(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

        if len(postData['fname']) < 2:
            errors.append('First name must be at least 2 characters long.')
        if len(postData['lname']) < 2:
            errors.append('Last name must be at least 2 characters long.')
        if not EMAIL_REGEX.match(postData['email']):
            errors.append('Please enter a valid email address.')

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
