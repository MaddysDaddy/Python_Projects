# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import bcrypt

import re

from django.core.exceptions import ObjectDoesNotExist

# Create your models here.


class UserManager(models.Manager):
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
            if postData['password'] != postData['confirm_password']:
                errors.append('Passwords do not match')

        return errors

    def create_user(self, postData):
        print postData
        pwhash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())

        user = User.objects.create(
            email=postData['email'],
            first_name=postData['first_name'],
            last_name=postData['last_name'],
            pwhash=pwhash
        )

        admin = User.objects.get(id=1)
        if admin:
            admin.user_level = 9
            admin.save()
        else:
            pass

        return user

    def update_user(self, postData, user_id):
        errors = []
        user = User.objects.get(id=user_id)
        EMAIL_REGEX = re.compile(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

        if 'first_name' in postData:
            if len(postData['first_name']) < 2:
                errors.append('First name must be at least 2 characters long.')
            else:
                user.first_name = postData['first_name']

        if 'last_name' in postData:
            if len(postData['last_name']) < 2:
                errors.append('Last name must be at least 2 characters long.')
            else:
                user.last_name = postData['last_name']

        if 'email' in postData:

            if user.email != postData['email']:
                if len(User.objects.filter(email=postData['email'])):
                    errors.append(
                        'This email address has already been registered. Please try again.')

            if not EMAIL_REGEX.match(postData['email']):
                errors.append('Please enter a valid email address.')
            else:
                user.email = postData['email']

        if 'description' in postData:
            user.description = postData['description']

        if 'user_level' in postData:
            user.user_level = postData['user_level']

        if 'password' in postData:
            if postData['password'] != postData['confirm_password']:
                errors.append('Passwords do not match')
            else:
                user.pwhash = bcrypt.hashpw(
                    postData['password'].encode(), bcrypt.gensalt())

        if errors:
            return errors
        else:
            user.save()
            return user

    def login(self, postData):
        email = postData['email']
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
    email = models.CharField(max_length=255)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    pwhash = models.CharField(max_length=255)
    user_level = models.IntegerField(default=1)
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class PostManager(models.Manager):
    def validate_post(self, postData):
        errors = []
        post = postData['message']

        if len(post) < 1:
            errors.append('Message cannot be empty.')
        return errors

    def create_post(self, postData, user_id, post_user_id):
        post = Post.objects.create(
            post=postData['message'],
            user=User.objects.get(id=user_id),
            from_user=User.objects.get(id=post_user_id)
        )
        return post


class Post(models.Model):
    post = models.TextField()
    user = models.ForeignKey(User, related_name="posts_user")
    from_user = models.ForeignKey(
        User, related_name='posts_from_user', default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PostManager()


class CommentManager(models.Manager):
    def validate_comment(self, postData):
        errors = []
        post = postData['comment']

        if len(post) < 1:
            errors.append('Message cannot be empty.')
        return errors

    def create_comment(self, postData, commenter_id, post_id):
        comment = Comment.objects.create(
            comment=postData['comment'],
            from_user=User.objects.get(id=commenter_id),
            post=Post.objects.get(id=post_id)
        )
        return comment


class Comment(models.Model):
    comment = models.TextField()
    from_user = models.ForeignKey(User, related_name="comments")
    post = models.ForeignKey(Post, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CommentManager()
