from django.shortcuts import render_to_response, get_object_or_404
from django.views import generic
from django.http import HttpResponse
from django.template import RequestContext

from erx.models import Patient, NewPatientForm, Prescription, NewPrescriptionForm, Rxnconso

#Create your views here.

#
#CRUD and Search methods for Patients
#

#Create new patient
def createPatient(request):
   
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
           return render_to_response('erx/new_patient.html', {'form': NewPatientForm}, context_instance=RequestContext(request))

#Read patient information
def getPatient(request, pk):
    pass

#Get all patients
def getAllPatient(request):
    pass

#Update patient information
def updatePatient(request):
    pass

#Delete patient information
def deletePatient(request):
    pass

#Search for patient in the database
def searchPatient(request):
    pass
#
#End of Patient methods
#

#
#CRUD & Search methods for Prescription
#

#Add new prescription
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

#Get prescription
def getPrescription(request):
    pass

#Get all prescriptions 
def getAllPrescriptions(request):
    pass

#Update prescription
def updatePrescription(request):
    pass

#Delete prescription
def deletePrescription(request):
    pass

#Search prescription
def searchPrescription(request):
    pass

#
#End of prescription methods
#

#
#Read & Search methods for Drugs in RxNorm
#

#Search for a drug in the database
def search(request, name):

    result = Rxnconso.objects.filter(str__contains=name)
    return render_to_response('erx/done.html', {'message': 'Drugs found:', 'list': result}, context_instance=RequestContext(request))


#Retrieve drug details based on the primary key
def select(request, rxaui):

    drug = str(get_object_or_404(Rxnconso, rxaui=rxaui).getDrug())
    return render_to_response('erx/done.html', {'message': drug.split()}, context_instance=RequestContext(request))


#Get all drugs in the database.
#Test only, do not use.
def getAll(request):

    drugs = Rxnconso.objects.all()
    return render_to_response('erx/done.html', {'message': 'All drugs:', 'list': drugs}, context_instance=RequestContext(request))
#
#End of drug methods
#
