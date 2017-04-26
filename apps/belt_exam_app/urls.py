from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register_account),
    url(r'^login$', views.login_account),
    url(r'^logout$', views.logout),
    url(r'^travels$', views.travels),
    url(r'^travels/add$', views.add_travel),
    url(r'^trip_add$', views.trip_add),
    url(r'^travels/destination/(?P<id>\d+)$', views.destination, name = 'destination'),
    url(r'^travels/join/(?P<id>\d+)$', views.join_trip, name = 'join'),
    url(r'^not_logged$', views.not_logged),
]
