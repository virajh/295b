from django.conf.urls import patterns, url

from erx import views

urlpatterns = patterns('',
    url(r'^newpatient/$', views.newpatient, name='new_patient'),
    url(r'^newprescription/$', views.newprescription, name='new_prescription'),
)

