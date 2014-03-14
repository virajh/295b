from django.shortcuts import render_to_response
from django.views import generic
from django.http import HttpResponse
from django.template import RequestContext

from erx.models import Patient, NewPatientForm, Prescription, NewPrescriptionForm

#erx Create your views here.

def newpatient(request):
   
    if request.method == "POST":
       form = NewPatientForm(request.POST)

       if form.is_valid():
           instance = form.save(commit=False)
           instance.save()
           return render_to_response('erx/done.html', {'message': "Patient Saved."}, context_instance=RequestContext(request))

       else:
           return render_to_response('erx/done.html', {'message': form.errors}, context_instance=RequestContext(request))

    else:

       if request.method == "GET":
           print "GET"
           return render_to_response('erx/new_patient.html', {'form': NewPatientForm}, context_instance=RequestContext(request))


def newprescription(request):

    if request.method == "POST":
        form = NewPrescriptionForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return render_to_response('erx/done.html', {'message': "Prescription Saved."}, context_instance=RequestContext(request))

        else:
            return render_to_response('erx/done.html', {'message': form.errors}, context_instance=RequestContext(request))

    else:
        if request.method == "GET":
            return render_to_response('erx/new_prescription.html', {'form': NewPrescriptionForm}, context_instance=RequestContext(request))
