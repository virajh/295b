from django.conf.urls import patterns, url

from erx import views

urlpatterns = patterns('',
    url(r'^newpatient/$', views.createPatient, name='new_patient'),
    url(r'^newprescription/$', views.newprescription, name='new_prescription'),
    url(r'^search/$', views.getAll, name='getAll'),
    url(r'^search/(?P<name>\w+)/$', views.search, name='search'),
    url(r'^select/(?P<rxaui>\d+)/$', views.select, name='select'),
)

