from django.conf.urls import patterns, url

from erx import views

urlpatterns = patterns('',
    url(r'^newpatient/$', views.newpatient, name='new_patient'),
    url(r'^newprescription/$', views.newprescription, name='new_prescription'),
    url(r'^search/(?P<name>\w+)/$', views.search, name='search'),
    url(r'^search/\w+/(?P<rxaui>\d+)/$', views.select, name='select'),
)

