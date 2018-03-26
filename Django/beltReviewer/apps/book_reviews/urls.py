from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.welcome, name='login'),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^books$', views.books),
    url(r'^books/(?P<book_id>\d+)$', views.book_detail),
    url(r'^add$', views.add_book, name='add_review'),
    url(r'^add_book_review$', views.add_book_and_review),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^(?P<book_id>\d+)/review$', views.add_review),
    url(r'^users/(?P<user_id>\d+)$', views.user_details),
    url(r'^(?P<book_id>\d+)/(?P<review_id>\d+)/delete$', views.delete_review)
]
