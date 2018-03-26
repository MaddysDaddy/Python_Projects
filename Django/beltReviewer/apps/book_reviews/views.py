# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponseRedirect

from . models import *

from django.contrib import messages

# Create your views here.


def welcome(request):
    if 'user' not in request.session:
        return render(request, 'book_reviews/welcome.html')
    else:
        return redirect('/books')


def login(request):
    if request.method == 'POST':
        user = User.objects.login(request.POST)

        if type(user) == User:
            request.session['user'] = user.id
            return redirect('/books')
        else:
            for error in user:
                messages.error(request, error)
            return redirect('/')


def register(request):
    if request.method == 'POST':
        errors = User.objects.user_validator(request.POST)

        if errors:
            for error in error:
                messages.error(request, error)
            return redirect('/')

        else:
            user = User.objects.create_user(request.POST)

            new_user = User.objects.get(id=user.id)
            request.session['user'] = new_user.id

            return redirect('/books')
    else:
        return redirect('/')


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


def books(request):
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
        return redirect('/')


def add_book(request):
    if 'user' in request.session:

        context = {
            'authors': Author.objects.all()
        }

        return render(request, 'book_reviews/add.html', context)

    else:
        return redirect('/')


def add_book_and_review(request):
    if request.method == 'POST':
        reviewer = User.objects.get(id=request.session['user'])
        book_review = Book.objects.create_book_and_review(
            request.POST, reviewer)

        print request.POST, reviewer
        print book_review
        return redirect('/add')


def delete_review(request, book_id, review_id):
    if request.method == "POST":
        Review.objects.delete_review(review_id)
        return redirect('/books/' + book_id)


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


def add_review(request, book_id):
    if request.method == 'POST':
        reviewer = request.session['user']

        errors = Review.objects.review_validator(request.POST)

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('/books/' + book_id)
        else:
            review = Review.objects.create_review(
                request.POST, book_id, reviewer)
            return redirect('/books/' + book_id)

    else:
        return redirect('/books/' + book_id)


def logout(request):
    request.session.pop('user')
    return redirect('/')
