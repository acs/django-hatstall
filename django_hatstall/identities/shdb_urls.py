from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^params$', views.get_shdb_params, name='params shdb'),
]
