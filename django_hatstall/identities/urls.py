from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='identities index'),
    url(r'^list$', views.list, name='identities list'),
    url(r'^(?P<identity_id>[0-f]+)/$', views.identity, name='show identity'),
    url(r'^(?P<identity_id>[0-f]+)/update_enrollment/(?P<organization>[0-9A-Za-z\w|\W]+)$', views.update_enrollment, name='update identity'),
    url(r'^(?P<identity_id>[0-f]+)/enroll_in/(?P<organization>[0-9A-Za-z\w|\W]+)$', views.enroll_to_profile, name='enroll identity'),
    url(r'^(?P<identity_id>[0-f]+)/unenroll_from/(?P<organization_info>[0-9A-Za-z\w|\W]+)$', views.unenroll_profile, name='unenroll identity'),
    url(r'^(?P<identity_id>[0-f]+)/merge$', views.merge_to_profile, name='merge to profile'),
    url(r'^(?P<profile_uuid>[0-f]+)/unmerge/(?P<identity_id>[0-f]+)$', views.unmerge, name='unmerge identity from a profile'),
]
