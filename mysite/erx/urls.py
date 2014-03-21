from django.conf.urls import patterns, url

from erx import views

urlpatterns = patterns('',

    url(r'^patient/$', views.getAllPatients, name='get_all_patients'),
    url(r'^patient/new/$', views.createPatient, name='new_patient'),
    url(r'^patient/delete/(?P<patient>\d{3}-\d{2}-\d{4})/$', views.deletePatient, name='delete_patient'),
    url(r'^patient/(?P<patient>\d{3}-\d{2}-\d{4})/$', views.handlePatient, name='handle_patient'),



    url(r'^newprescription/$', views.newprescription, name='new_prescription'),

    url(r'^newpharmacy/$', views.newpharmacy, name='new_pharmacy'),
    url(r'^search/$', views.getAll, name='getAll'),
    url(r'^search/(?P<name>\w+)/$', views.search, name='search'),
    url(r'^select/(?P<rxaui>\d+)/$', views.select, name='select'),
)
