# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse, HttpResponseRedirect

from . models import *
from ..users.models import *

from django.contrib import messages

# Create your views here.


def index(request):
    if 'user' in request.session:
        current_user = User.objects.get(id=request.session['user'])

        context = {
            'user': current_user,
            'books': Book.objects.order_by('created_at').reverse()[:5],
            'reviews': Review.objects.all(),
            'all_books': Book.objects.all()
        }
        return render(request, 'book_reviews/books.html', context)

    else:
        return redirect(reverse('login:index'))

# Open the form that will allow the logged in user to add a new book and review


def add_book(request):
    if 'user' in request.session:

        context = {
            'authors': Author.objects.all()
        }

        return render(request, 'book_reviews/add.html', context)

    else:
        return redirect('/')

# Add a new book and review to the database


def add_book_and_review(request):
    if request.method == 'POST':
        reviewer = User.objects.get(id=request.session['user'])
        book_review = Book.objects.create_book_and_review(
            request.POST, reviewer)

        print request.POST, reviewer
        print book_review
        # return redirect('/add_book')
        return HttpResponseRedirect(reverse('reviews:add_book'))


# Add detail view for individual books
def book_detail(request, book_id):
    if 'user' in request.session:

        book = Book.objects.get(id=book_id)
        context = {
            'book': book,
            'authors': book.authors.all(),
            'reviews': Review.objects.filter(book__id=book_id)
        }
        print context
        return render(request, 'book_reviews/book.html', context)

    else:
        return redirect('/')


# Add a review in book detail view
def add_review(request, book_id):
    if request.method == 'POST':
        reviewer = request.session['user']

        errors = Review.objects.review_validator(request.POST)

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('reviews:book_detail', book_id=book_id)
        else:
            review = Review.objects.create_review(
                request.POST, book_id, reviewer)
            print '/' + book_id + '/book'
            return redirect('reviews:book_detail', book_id=book_id)

    else:
        return redirect('reviews:book_detail', book_id=book_id)


# Delete a review if you are the one who wrote it
def delete_review(request, book_id, review_id):
    if request.method == "POST":
        Review.objects.delete_review(review_id)
        return redirect('reviews:book_detail', book_id=book_id)


# View details about the reviewer
def user_details(request, user_id):
    if 'user' in request.session:
        total_reviews = len(Review.objects.filter(reviewer__id=user_id))
        context = {
            'user': User.objects.get(id=user_id),
            'reviews': Review.objects.filter(reviewer__id=user_id),
            'total_reviews': total_reviews
        }
        return render(request, 'book_reviews/users.html', context)
    else:
        return redirect('/')
