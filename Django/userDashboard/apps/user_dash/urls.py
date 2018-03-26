from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signin$', views.login, name='login'),
    url(r'^user_login$', views.user_login),
    url(r'^register$', views.register, name='register'),
    url(r'^create$', views.create),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^users/show/(?P<user_id>\d+)$', views.user_details, name='show_user'),
    url(r'^users/show/(?P<user_id>\d+)/message$',
        views.message, name='message'),
    url(r'^(?P<user_id>\d+)/comment/(?P<post_id>\d+)$', views.comment),
    url(r'^(?P<user_id>\d+)/profile$', views.profile, name='profile'),
    url(r'^(?P<user_id>\d+)/profile/update$', views.profile_update)
]
