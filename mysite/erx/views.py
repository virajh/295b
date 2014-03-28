import sys, copy

from django.shortcuts import render_to_response, get_object_or_404
from django.views import generic
from django.http import HttpResponse
from django.template import RequestContext

from erx.models import NewPatientForm, ContactForm, PatientForm, NewPharmacyForm, PharmacyForm, PrescriptionForm
from erx.models import Patient, Contact, Pharmacy, NewPatient, Rxnconso

#Create your views here.

#
#CRUD and Search methods for Patients
#

#Create new patient
def createPatient(request):

    if request.method == "POST":
       form = NewPatientForm(request.POST)

       if form.is_valid():
           patient = PatientForm(request.POST)
           contact = ContactForm(request.POST)
           patient.save()
           contact.save()
           return render_to_response('erx/done.html', {'message': "Patient Saved."}, context_instance=RequestContext(request))
       else:
           return render_to_response('erx/done.html', {'message': form.errors}, context_instance=RequestContext(request))
    else:
       if request.method == "GET":
           return render_to_response('erx/new_patient.html', {'form': NewPatientForm}, context_instance=RequestContext(request))


#Get all patients
def getAllPatients(request):

    if request.method == 'GET':
        patients = Patient.objects.all()
        return render_to_response('erx/done.html', {'message': 'All patients:', 'patients': patients},
            context_instance=RequestContext(request))
    else:
        return render_to_response('erx/done.html', {'message': 'Not allowed.'},
            context_instance=RequestContext(request))

#Handle patient URL
def handlePatient(request, patient_uid):

    if request.method == 'GET':
        patient = get_object_or_404(Patient, uid=patient_uid)
        form = PatientForm(instance=patient)
        return render_to_response('erx/form.html', {'message': 'Patient found',
                                                    'form': form},
            context_instance=RequestContext(request))

    if request.method == 'POST':

        if 'update' in request.POST:
            patient = get_object_or_404(Patient, uid=patient_uid)
            form = PatientForm(request.POST, instance=patient)
            if form.is_valid():
                form.save()
                return render_to_response('erx/done.html', {'message': 'Patient %s saved.' % (patient)},
                    context_instance=RequestContext(request))
            else:
                return render_to_response('erx/done.html', {'message': 'Patient %s not saved.\nErrors: %s ' % (patient, form.errors)},
                    context_instance=RequestContext(request))
        else:#to do
            if 'delete' in request.POST:
                try:
                    Patient.objects.filter(uid=patient_uid).delete()
                    return render_to_response('erx/done.html', {'message': 'Patient %s deleted.' % (patient_uid)},
                        context_instance=RequestContext(request))
                except Exception as e:
                    return render_to_response('erx/done.html', {'message': e},
                        context_instance=RequestContext(request))

#
#End of Patient methods
#

#
#CRUD & Search methods for Prescription
#

#Add new prescription
def newprescription(request):

    if request.method == "POST":
        form = PrescriptionForm(request.POST)

        if form.is_valid():
            form.save
            return render_to_response('erx/done.html', {'message': "Prescription Saved."}, context_instance=RequestContext(request))

        else:
            return render_to_response('erx/done.html', {'message': form.errors}, context_instance=RequestContext(request))
    else:
        if request.method == "GET":
            return render_to_response('erx/new_prescription.html', {'form': PrescriptionForm}, context_instance=RequestContext(request))

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
#Pharmacy CRUD & Search Methods
#

#Create pharmacy
def createPharmacy(request):

    if request.method == 'POST':
        form = NewPharmacyForm(request.POST)

        if form.is_valid():
            pharmacy = PharmacyForm(request.POST)
            contact = ContactForm(request.POST)
            pharmacy.save()
            contact.save()
            return render_to_response('erx/done.html', {'message': "Pharmacy Saved."}, context_instance=RequestContext(request))
        else:
            return render_to_response('erx/done.html', {'message': form.errors}, context_instance=RequestContext(request))
    else:
       if request.method == "GET":
           return render_to_response('erx/new_pharmacy.html', {'form': NewPharmacyForm}, context_instance=RequestContext(request))

#Get all Pharmacy
def getAllPharmacy(request):

    if request.method == 'GET':
        pharmacies = Pharmacy.objects.all()
        return render_to_response('erx/done.html', {'message': 'All pharmacies:', 'pharmacies': pharmacies},
            context_instance=RequestContext(request))
    else:
        return render_to_response('erx/done.html', {'message': 'Not allowed.'},
            context_instance=RequestContext(request))

#Handle pharmacy
def handlePharmacy(request, pharmacy_uid):

    if request.method == 'GET':
        pharmacy = get_object_or_404(Pharmacy, uid=pharmacy_uid)
        form = PharmacyForm(instance=pharmacy)
        return render_to_response('erx/form.html', {'message': 'Pharmacy found',
                                                    'form': form},
            context_instance=RequestContext(request))

    if request.method == 'POST':
        if 'update' in request.POST:
            pharmacy = get_object_or_404(Pharmacy, uid=pharmacy_uid)
            form = PharmacyForm(request.POST, instance=pharmacy)
            if form.is_valid():
                form.save()
                return render_to_response('erx/done.html', {'message': 'Pharmacy %s saved.' % (pharmacy)},
                    context_instance=RequestContext(request))
            else:
                return render_to_response('erx/done.html', {'message': 'Pharmacy %s not saved.\nErrors: %s ' % (pharmacy, form.errors)},
                    context_instance=RequestContext(request))
        else:#to do
            if 'delete' in request.POST:
                try:
                    Pharmacy.objects.filter(uid=pharmacy_uid).delete()
                    return render_to_response('erx/done.html', {'message': 'Pharmacy %s deleted.' % (pharmacy_uid)},
                        context_instance=RequestContext(request))
                except Exception as e:
                    return render_to_response('erx/done.html', {'message': e},
                        context_instance=RequestContext(request))
#
#End of Pharmacy methods
#

#
#Read & Search methods for Drugs in RxNorm
#

#Search for a drug in the database
def search(request, name):

    result = Rxnconso.objects.filter(str__contains=name)
    if len(result) > 0:
        return render_to_response('erx/done.html', {'message': 'Drugs found:', 'list': result}, context_instance=RequestContext(request))
    else:
        return render_to_response('erx/done.html', {'message': 'Drug not found:'}, context_instance=RequestContext(request))

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
