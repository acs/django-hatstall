from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='identities index'),
    url(r'^list$', views.list, name='identities list'),
    url(r'^(?P<identity_id>[0-f]+)/$', views.identity, name='show identity'),
    url(r'^(?P<identity_id>[0-f]+)/update_enrollment/(?P<organization>[0-9A-Za-z\w|\W]+)$', views.update_enrollment, name='show identity'),
    url(r'^(?P<identity_id>[0-f]+)/unenroll_from/(?P<organization_info>[0-9A-Za-z\w|\W]+)$', views.unenroll_profile, name='show identity'),
]
