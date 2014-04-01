from django.conf.urls import patterns, url

from erx import views

urlpatterns = patterns('',

    url(r'^prescriber/$', views.getAllPrescriber, name='get_all_prescriber'),
    url(r'^prescriber/new/$', views.createPrescriber, name='new_prescriber'),
    url(r'^prescriber/(?P<prescriber_id>\w+)/$', views.handlePrescriber, name='handle_prescriber'),

    url(r'^patient/$', views.getAllPatients, name='get_all_patients'),
    url(r'^patient/new/$', views.createPatient, name='new_patient'),
    url(r'^patient/prescriber/(?P<p_id>\w+)/$', views.getPatientByPrescriber, name='get_patient_by_prescriber'),
    url(r'^patient/(?P<patient_id>\w+)/$', views.handlePatient, name='handle_patient'),

    url(r'^pharmacy/$', views.getAllPharmacy, name='get_all_pharmacy'),
    url(r'^pharmacy/new/$', views.createPharmacy, name='new_pharmacy'),
    url(r'^pharmacy/(?P<pharmacy_id>\w+)/$', views.handlePharmacy, name='handle_pharmacy'),

    url(r'^rx/$', views.getAllPrescription, name='get_all_prescription'),
    url(r'^rx/new/$', views.createPrescription, name='new_prescription'),
    url(r'^rx/(?P<rx_id>\w+)/$', views.handlePrescription, name='handle_prescription'),
    url(r'^rx/prescriber/(?P<p_id>\w+)/$', views.getPrescriptionByPrescriber, name='get_prescription_by_prescriber'),
    url(r'^rx/patient/(?P<p_id>\w+)/$', views.getPrescriptionByPatient, name='get_prescription_by_patient'),

    url(r'^search/$', views.getAll, name='getAll'),
    url(r'^search/(?P<name>\w+)/$', views.search, name='search'),
    url(r'^select/(?P<rxaui>\d+)/$', views.select, name='select'),
)
