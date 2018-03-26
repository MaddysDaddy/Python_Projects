# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
#from ..user.models import User

import re

import bcrypt

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
            if len(postData['name']) < 2:
                errors.append('Name must be at least 2 characters long.')
            if len(postData['alias']) < 2:
                errors.append('Alias must be at least 2 characters long.')
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
            name=postData['name'],
            alias=postData['alias'],
            email=postData['email'],
            pwhash=pwhash
        )

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
    name = models.CharField(max_length=30)
    alias = models.CharField(max_length=30)
    email = models.CharField(max_length=255)
    pwhash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class BookManager(models.Manager):
    def create_book_and_review(self, postData, reviewer):
        print postData['new_author']

        if postData['new_author']:
            author = Author.objects.create(
                name=postData['new_author']
            )
        else:
            author = Author.objects.get(name=postData['author'])

        book = Book.objects.create(
            title=postData['title'],
        )
        book.authors.add(author)
        book.save()

        new_book = Book.objects.get(id=book.id)

        review = Review.objects.create(
            review=postData['review'],
            stars=postData['stars'],
            reviewer=reviewer,
            book=new_book
        )

        return book, review


class Book(models.Model):
    title = models.CharField(max_length=255)
    #author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BookManager()


class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    books = models.ManyToManyField(Book, related_name="authors")


class ReviewManager(models.Manager):
    def review_validator(self, postData):
        errors = []
        if not postData['stars']:
            errors.append(
                'Please select how many stars to give you review. Minimum 1.')
        if not postData['review']:
            errors.append('Review section cannot be blank.')

        return errors

    def create_review(self, postData, book_id, reviewer):
        review = Review.objects.create(
            review=postData['review'],
            stars=postData['stars'],
            reviewer=User.objects.get(id=reviewer),
            book=Book.objects.get(id=book_id)
        )
        return review

    def delete_review(self, review_id):
        review = Review.objects.get(id=review_id)
        review.delete()


class Review(models.Model):
    review = models.TextField()
    stars = models.IntegerField()
    reviewer = models.ForeignKey(User, related_name="reviews")
    book = models.ForeignKey(Book, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ReviewManager()
