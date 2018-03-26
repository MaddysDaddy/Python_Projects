from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_book$', views.add_book, name='add_book'),
    url(r'^add_book_review$', views.add_book_and_review, name='add_book_review'),
    url(r'^(?P<book_id>\d+)/book$',
        views.book_detail, name='book_detail'),
    url(r'^(?P<book_id>\d+)/add_review$', views.add_review, name='add_review'),
    url(r'^(?P<book_id>\d+)/(?P<review_id>\d+)/delete$',
        views.delete_review, name='delete_review'),
    url(r'^user/(?P<user_id>\d+)$', views.user_details, name='user_detail')
]
