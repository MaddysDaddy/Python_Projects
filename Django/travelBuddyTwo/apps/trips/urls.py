from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.main, name="main"),
    url(r'^addplan$', views.addplan, name='addplan'),
    url(r'^addtrip$', views.addtrip, name='addtrip'),
    url(r'^destination/(?P<trip_id>\d+)$',
        views.destination, name='destination'),
    url(r'^(?P<trip_id>\d+)/join$', views.join, name='join')
]
