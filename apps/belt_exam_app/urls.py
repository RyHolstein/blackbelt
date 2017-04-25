from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register_account),
    url(r'^login$', views.login_account),
    # url(r'^logout$', views.logout),
]
