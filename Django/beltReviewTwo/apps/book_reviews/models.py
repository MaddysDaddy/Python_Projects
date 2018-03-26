# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..users.models import User
# Create your models here.


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
