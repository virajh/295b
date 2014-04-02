import sys, copy

from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response, get_object_or_404
from django.views import generic
from django.http import HttpResponse
from django.template import RequestContext

from erx.models import Prescriber, Patient, Pharmacy, Prescription, RxEntry#, Rxnconso
from erx.forms import PrescriberForm, PatientForm, PharmacyForm, PrescriptionForm, RxEntryForm

#Create your views here.

#
#CRUD & Search methods for Prescriber
#

#create new prescriber
def createPrescriber(request):

    if request.method == 'POST':
        form = PrescriberForm(request.POST)

        if form.is_valid():
            form.save()
            return render_to_response('erx/done.html', {'message': "Prescriber saved."}, context_instance=RequestContext(request))

        else:
            return render_to_response('erx/done.html', {'message': form.errors}, context_instance=RequestContext(request))

    else:
       if request.method == "GET":
           return render_to_response('erx/new_doctor.html', {'form': PrescriberForm, 'formType': 'user'}, context_instance=RequestContext(request))


#get all prescribers
def getAllPrescriber(request):

    if request.method == 'GET':
        prescribers = Prescriber.objects.all()
        return render_to_response('erx/done.html', {'message': 'All prescribers', 'prescribers': prescribers},
            context_instance=RequestContext(request))
    else:
        return render_to_response('erx/done.html', {'message': 'Not allowed.'},
                                  context_instance=RequestContext(request))


#handle prescriber: GET, POST, DELETE
def handlePrescriber(request, prescriber_id):

    if request.method == 'GET':
        prescriber = get_object_or_404(Prescriber, prescriber_id=prescriber_id)
        form = PrescriberForm(instance=prescriber)
        return render_to_response('erx/form.html', {'message': 'Prescriber found',
                                                    'form': form},
            context_instance=RequestContext(request))

    if request.method == 'POST':

        if 'update' in request.POST:
            prescriber = get_object_or_404(Prescriber, prescriber_id=prescriber_id)
            form = PrescriberForm(request.POST, instance=prescriber)
            if form.is_valid():
                form.save()
                return render_to_response('erx/done.html', {'message': 'Prescriber %s saved.' % (prescriber)},
                    context_instance=RequestContext(request))
            else:
                return render_to_response('erx/done.html', {'message': 'Prescriber %s not saved.\nErrors: %s ' % (prescriber, form.errors)},
                    context_instance=RequestContext(request))
        else:
            if 'delete' in request.POST:
                try:
                    Prescriber.objects.filter(prescriber_id=prescriber_id).delete()
                    return render_to_response('erx/done.html', {'message': 'Prescriber %s deleted.' % (prescriber_id)},
                        context_instance=RequestContext(request))
                except Exception as e:
                    return render_to_response('erx/done.html', {'message': e},
                        context_instance=RequestContext(request))

#
#End of Prescriber Methods
#


#
#CRUD and Search methods for Patients
#

#Create new patient
def createPatient(request):

    if request.method == "POST":
       form = PatientForm(request.POST)

       if form.is_valid():
           form.save()
           return render_to_response('erx/done.html', {'message': "Patient saved."}, context_instance=RequestContext(request))

       else:
           return render_to_response('erx/done.html', {'message': form.errors}, context_instance=RequestContext(request))

    else:
       if request.method == "GET":
           return render_to_response('erx/new_patient.html', {'form': PatientForm}, context_instance=RequestContext(request))


#Get all patients
def getAllPatients(request):

    if request.method == 'GET':
        patients = Patient.objects.all()
        return render_to_response('erx/done.html', {'message': 'All patients:', 'patients': patients},
            context_instance=RequestContext(request))
    else:
        return render_to_response('erx/done.html', {'message': 'Not allowed.'},
            context_instance=RequestContext(request))


#Handle patient: GET, POST, DELETE
def handlePatient(request, patient_id):

    if request.method == 'GET':
        patient = get_object_or_404(Patient, patient_id=patient_id)
        form = PatientForm(instance=patient)
        return render_to_response('erx/form.html', {'message': 'Patient found',
                                                    'form': form},
            context_instance=RequestContext(request))

    if request.method == 'POST':

        if 'update' in request.POST:
            patient = get_object_or_404(Patient, patient_id=patient_id)
            form = PatientForm(request.POST, instance=patient)
            if form.is_valid():
                form.save()
                return render_to_response('erx/done.html', {'message': 'Patient %s saved.' % (patient)},
                    context_instance=RequestContext(request))
            else:
                return render_to_response('erx/done.html', {'message': 'Patient %s not saved.\nErrors: %s ' % (patient, form.errors)},
                    context_instance=RequestContext(request))
        else:
            if 'delete' in request.POST:
                try:
                    Patient.objects.filter(patient_id=patient_id).delete()
                    return render_to_response('erx/done.html', {'message': 'Patient deleted.'},
                        context_instance=RequestContext(request))
                except Exception as e:
                    return render_to_response('erx/done.html', {'message': e},
                        context_instance=RequestContext(request))


#get patients by prescriber
def getPatientByPrescriber(request, p_id):

    if request.method == 'GET':
        prescriber = get_object_or_404(Prescriber, prescriber_id=p_id)
        patient_list = Patient.objects.filter(prescriber=prescriber)

        if patient_list.count() > 0:
            return render_to_response('erx/done.html', {'message': 'Patient of %s:' % (prescriber),
                                                        'patients': patient_list},
                context_instance=RequestContext(request))

        else:
            return render_to_response('erx/done.html', {'message': 'No patients found for %s.' % (prescriber)},
                context_instance=RequestContext(request))
    else:
        return render_to_response('erx/done.html', {'message': 'Not allowed.'},
            context_instance=RequestContext(request))
#
#End of Patient methods
#


#
#Pharmacy CRUD & Search Methods
#

#Create pharmacy
def createPharmacy(request):

    if request.method == 'POST':
        form = PharmacyForm(request.POST)

        if form.is_valid():
            form.save()
            return render_to_response('erx/done.html', {'message': "Pharmacy Saved."}, context_instance=RequestContext(request))

        else:
            return render_to_response('erx/done.html', {'message': form.errors}, context_instance=RequestContext(request))

    else:
       if request.method == "GET":
           return render_to_response('erx/new_pharmacy.html', {'form': PharmacyForm}, context_instance=RequestContext(request))


#Get all Pharmacy
def getAllPharmacy(request):

    if request.method == 'GET':
        pharmacies = Pharmacy.objects.all()
        return render_to_response('erx/done.html', {'message': 'All pharmacies:', 'pharmacies': pharmacies},
            context_instance=RequestContext(request))
    else:
        return render_to_response('erx/done.html', {'message': 'Not allowed.'},
            context_instance=RequestContext(request))


#Handle pharmacy: GET, POST, DELETE
def handlePharmacy(request, pharmacy_id):

    if request.method == 'GET':
        pharmacy = get_object_or_404(Pharmacy, pharmacy_id=pharmacy_id)
        form = PharmacyForm(instance=pharmacy)
        return render_to_response('erx/form.html', {'message': 'Pharmacy found',
                                                    'form': form},
            context_instance=RequestContext(request))

    if request.method == 'POST':
        if 'update' in request.POST:
            pharmacy = get_object_or_404(Pharmacy, pharmacy_id=pharmacy_id)
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
                    Pharmacy.objects.filter(pharmacy_id=pharmacy_id).delete()
                    return render_to_response('erx/done.html', {'message': 'Pharmacy deleted.'},
                        context_instance=RequestContext(request))
                except Exception as e:
                    return render_to_response('erx/done.html', {'message': e},
                        context_instance=RequestContext(request))
#
#End of Pharmacy methods
#


#
#CRUD & Search methods for Prescription
#

#create new prescription
def createPrescription(request):

    if request.method == "POST":
        form = PrescriptionForm(request.POST)

        if form.is_valid():
            instance=form.save()
            rxentry = RxEntryForm(request.POST, instance=instance)
            
            if rxentry.is_valid():
                rxentry.save()
                return render_to_response('erx/done.html', {'message': "Prescription created."}, context_instance=RequestContext(request))

            else:
                return render_to_response('erx/done.html', {'message': rxentry.errors}, context_instance=RequestContext(request))

        else:
            return render_to_response('erx/done.html', {'message': form.errors}, context_instance=RequestContext(request))

    else:
        if request.method == "GET":
            return render_to_response('erx/new_prescription.html',
                {'form': PrescriptionForm, 'rxform': RxEntryForm}, context_instance=RequestContext(request))


#get all prescription
def getAllPrescription(request):

    if request.method == 'GET':
        prescriptions = Prescription.objects.all()
        return render_to_response('erx/done.html', {'message': 'All prescriptions:', 'prescriptions': prescriptions},
            context_instance=RequestContext(request))
    else:
        return render_to_response('erx/done.html', {'message': 'Not allowed.'},
            context_instance=RequestContext(request))


#handle prescription: GET using ID, POST, DELETE
def handlePrescription(request, rx_id):

    if request.method == 'GET':
        rx = get_object_or_404(Prescription, rx_id=rx_id)

        form = PrescriptionForm(instance=rx)
        rxforms = RxEntryForm(instance=rx)

        return render_to_response('erx/cur_prescription.html', {'message': 'Prescription found',
                                                    'form': form, 'rxform': rxforms},
            context_instance=RequestContext(request))

    if request.method == 'POST':
        rx = get_object_or_404(Prescription, rx_id=rx_id)

        if 'update' in request.POST:            
            form = PrescriptionForm(request.POST, instance=rx)

            if form.is_valid():
                instance=form.save()
                rxentry = RxEntryForm(request.POST, instance=instance)

                if rxentry.is_valid():
                    rxentry.save()
                    return render_to_response('erx/done.html', {'message': 'Prescription %s updated.' % (rx)},
                                              context_instance=RequestContext(request))
                else:
                    return render_to_response('erx/done.html', {'message': rxentry.errors}, context_instance=RequestContext(request))
            else:
                return render_to_response('erx/done.html', {'message': 'Prescription %s not saved.\nErrors: %s ' % (rx, form.errors)},
                    context_instance=RequestContext(request))

        else:
            if 'delete' in request.POST:
                try:
                    RxEntry.objects.filter(prescription=rx).delete()
                    Prescription.objects.filter(rx_id=rx_id).delete()
                    return render_to_response('erx/done.html', {'message': 'Prescription deleted.'},
                        context_instance=RequestContext(request))
                except Exception as e:
                    return render_to_response('erx/done.html', {'message': e},
                        context_instance=RequestContext(request))


#get prescriptions by prescriber
def getPrescriptionByPrescriber(request, p_id):

    if request.method == 'GET':
        prescriber = get_object_or_404(Prescriber, prescriber_id=p_id)
        prescriptions = Prescription.objects.filter(prescriber=prescriber)

        if prescriptions.count() > 0:
            return render_to_response('erx/done.html', {'message': 'Prescriptions found for %s:' % (prescriber),
                                                        'prescriptions': prescriptions},
                context_instance=RequestContext(request))

        else:
            return render_to_response('erx/done.html', {'message': 'No prescriptions found for %s.' % (prescriber)},
                context_instance=RequestContext(request))
    else:
        return render_to_response('erx/done.html', {'message': 'Not allowed.'},
            context_instance=RequestContext(request))


#get prescriptions by patient
def getPrescriptionByPatient(request, p_id):

    if request.method == 'GET':
        patient = get_object_or_404(Patient, patient_id=p_id)
        prescriptions = Prescription.objects.filter(patient=patient)

        if prescriptions.count() > 0:
            return render_to_response('erx/done.html', {'message': 'Prescriptions found for %s:' % (patient),
                                                        'prescriptions': prescriptions},
                context_instance=RequestContext(request))

        else:
            return render_to_response('erx/done.html', {'message': 'No prescriptions found for %s.' % (patient)},
                context_instance=RequestContext(request))
    else:
        return render_to_response('erx/done.html', {'message': 'Not allowed.'},
            context_instance=RequestContext(request))

#
#End of prescription methods
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
