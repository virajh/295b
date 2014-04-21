import sys, copy

from time import strftime

from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views import generic


from erx.forms import PrescriberForm, PatientForm, PharmacyForm, PrescriptionForm, RxEntryForm, LabTestForm, LabHistoryForm
from erx.models import Prescriber, Patient, Pharmacy, Prescription, RxEntry, LabTest, LabHistory
#from erx.models import Rxnconso

#Create your views here.

def testView(request, **kwargs):

    if 'message' in kwargs:
        message = kwargs['message']
    else:
        message = ""

    patient = Patient.objects.all()[2]
    fields = list(PatientForm(instance=patient))
    p_profile,p_med, p_contact = fields[1:7], fields[7:12],fields[12:]
    prescriptions = Prescription.objects.filter(patient=patient)

    labhist = LabHistoryForm(instance=LabHistory(patient=patient))
    return render_to_response('erx/bootstrap.html', {'patient': patient, 'p_contact': p_contact, 'message': message,
                                                     'p_profile': p_profile, 'p_all': fields, 'p_med': p_med,
                                                     'prescriptions': prescriptions, 'p_lab_hist': labhist},
                              context_instance=RequestContext(request))


#
#CRUD & Search methods for Prescriber
#

#prescriber patient view
def prescriberPatient(request, p_id, **kwargs):

    if 'message' in kwargs:
        message = kwargs['message']
    else:
        message = ""

    patient = Patient.objects.get(patient_id=p_id)
    fields = list(PatientForm(instance=patient))
    p_profile,p_med, p_contact = fields[1:7], fields[7:12],fields[12:]
    prescriptions = Prescription.objects.filter(patient=patient)

    labhist = LabHistoryForm(instance=LabHistory(patient=patient))
    return render_to_response('erx/prescriber_patient.html', {'patient': patient, 'p_contact': p_contact, 'message': message,
                                                              'p_profile': p_profile, 'p_all': fields, 'p_med': p_med,
                                                              'prescriptions': prescriptions, 'p_lab_hist': labhist},
                              context_instance=RequestContext(request))


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
        fields = list(form)
        p_basic, p_contact = fields[:5], fields[5:]
        return render_to_response('erx/new_prescriber.html', {'prescriber': prescriber, 'p_basic': p_basic, 'p_contact': p_contact},
            context_instance=RequestContext(request))

    if request.method == 'POST':

#        if 'update' in request.POST:
        prescriber = get_object_or_404(Prescriber, prescriber_id=prescriber_id)
        form = PrescriberForm(request.POST, instance=prescriber)
        if form.is_valid():
            form.save()
            return prescriberHome(request, prescriber=prescriber_id,
                message="[%s] Prescriber %s profile modified successfully." % (strftime("%Y-%m-%d %H:%M:%S"), prescriber))
        else:
            fields = list(form)
            p_basic, p_contact = fields[:5], fields[5:]
            return render_to_response('erx/new_prescriber.html',
                {'prescriber': prescriber, 'p_basic': p_basic, 'p_contact': p_contact,
                 'message': '[%s] Prescriber %s not saved. Errors: %s ' % (strftime("%Y-%m-%d %H:%M:%S"), prescriber, form.errors)},
                context_instance=RequestContext(request))

#        else:
#            if 'delete' in request.POST:
#                try:
#                    Prescriber.objects.filter(prescriber_id=prescriber_id).delete()
#                    return render_to_response('erx/done.html', {'message': 'Prescriber %s deleted.' % (prescriber_id)},
#                        context_instance=RequestContext(request))
#                except Exception as e:
#                    return render_to_response('erx/done.html', {'message': e},
#                        context_instance=RequestContext(request))

#prescriber home
def prescriberHome(request, **kwargs):

    prescriber = Prescriber.objects.all()[0]
    my_profile = PrescriberForm(instance=prescriber)
    my_patients = Patient.objects.filter(prescriber=prescriber)
    pending = Prescription.objects.filter(prescriber=prescriber, status="PENDING")
    submitted = Prescription.objects.filter(prescriber=prescriber, status="SUBMITTED")
    dispensed = Prescription.objects.filter(prescriber=prescriber, status="DISPENSED")

    if 'message' in kwargs:
        message = kwargs['message']
    else:
        message = ''

    return render_to_response('erx/prescriber_home.html', {'prescriber': prescriber, 'my_profile': my_profile, 'message':message,
                                                           'my_patients': my_patients, 'pending': pending,
                                                           'submitted': submitted, 'dispensed': dispensed},
                              context_instance=RequestContext(request))
#
#End of Prescriber Methods
#


#
#CRUD and Search methods for Patients
#

#Create new patient for prescriber
def createPatientForPrescriber(request, p_id):

    if request.method == "POST":
       form = PatientForm(request.POST)

       if form.is_valid():
           patient=form.save()
           prescriber = get_object_or_404(Prescriber, prescriber_id=p_id)
           my_profile = PrescriberForm(instance=prescriber)
           my_patients = Patient.objects.filter(prescriber=prescriber)
           pending = Prescription.objects.filter(prescriber=prescriber, status="PENDING")
           submitted = Prescription.objects.filter(prescriber=prescriber, status="SUBMITTED")
           dispensed = Prescription.objects.filter(prescriber=prescriber, status="DISPENSED")

           return render_to_response('erx/prescriber_home.html',
                {'prescriber': prescriber, 'my_profile': my_profile, 'my_patients': my_patients,
                 'pending': pending, 'submitted': submitted, 'dispensed': dispensed,
                 'message': '[%s] Patient %s successfully created.' %(strftime("%Y-%m-%d %H:%M:%S"), patient)},
                              context_instance=RequestContext(request))

       else:
           prescriber = Prescriber.objects.get(prescriber_id = p_id)
           fields = list(form)
           p_basic = fields[:7]
           p_med = fields[7:12]
           p_contact = fields[12:]
           return render_to_response('erx/new_patient.html',
                {'p_basic': p_basic, 'p_med': p_med,'p_contact': p_contact,
                 'message': '[%s] Patient creation failed. Errors: %s' % (strftime("%Y-%m-%d %H:%M:%S"), form.errors)},
            context_instance=RequestContext(request))

    else:
       if request.method == "GET":
           prescriber = Prescriber.objects.get(prescriber_id = p_id)
           patient = Patient(prescriber=prescriber)
           form = PatientForm(instance=patient)
           fields = list(form)
           p_basic = fields[:7]
           p_med = fields[7:12]
           p_contact = fields[12:]
           return render_to_response('erx/new_patient.html',{'p_basic': p_basic, 'p_med': p_med,'p_contact': p_contact},
                                     context_instance=RequestContext(request))


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
           fields = list(form)
           p_basic = fields[:7]
           p_med = fields[7:12]
           p_contact = fields[12:]
           return render_to_response('erx/update_patient.html',
                                     {'patient': patient,'p_basic': p_basic, 'p_med': p_med,
                                      'p_contact': p_contact, 'form': form},
                                     context_instance=RequestContext(request))

    if request.method == 'POST':

        #if 'update' in request.POST:
        patient = get_object_or_404(Patient, patient_id=patient_id)
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return prescriberPatient(request, p_id=patient_id,
                message='[%s] Patient profile for %s updated successfully.' % (strftime("%Y-%m-%d %H:%M:%S"), patient))
        else:
            fields = list(form)
            p_basic = fields[:7]
            p_med = fields[7:12]
            p_contact = fields[12:]
            return render_to_response('erx/update_patient.html',
                    {'patient': patient,'p_basic': p_basic, 'p_med': p_med,
                     'p_contact': p_contact, 'form': form,
                     'message': '[%s] Patient %s not saved. Errors: %s' %
                        (strftime("%Y-%m-%d %H:%M:%S"), patient, form.errors)},
                context_instance=RequestContext(request))

        #else:
        #    if 'delete' in request.POST:
        #        patient = Patient.objects.get(patient_id=patient_id)
        #        try:
        #            Patient.objects.filter(patient_id=patient_id).delete()
        #            return prescriberHome(request, patient=patient_id, message='%s Patient profile for %s deleted successfully.' % (strftime("%Y-%m-%d %H:%M:%S"), patient))
        #        except Exception as e:
        #            return render_to_response('erx/done.html', {'message': e},
        #                context_instance=RequestContext(request))


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
  

#pharmacy home
def pharmacyHome(request, **kwargs):

    if 'message' in kwargs:
        message = kwargs['message']
    else:
        message = ""

    pharmacy = Pharmacy.objects.all()[0]
    my_profile = PharmacyForm(instance=pharmacy)
    new_p = Prescription.objects.filter(pharmacy=pharmacy, status="SUBMITTED")
    old_p = Prescription.objects.filter(pharmacy=pharmacy, status="DISPENSED")

    return render_to_response('erx/pharmacy_home.html', {'pharmacy': pharmacy, 'my_profile': my_profile,
                                                         'new_p': new_p, 'old_p': old_p, 'message': message},
                              context_instance=RequestContext(request))

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
        return render_to_response('erx/new_pharmacy.html', {'pharmacy': pharmacy, 'form': form},
            context_instance=RequestContext(request))

    if request.method == 'POST':
        pharmacy = get_object_or_404(Pharmacy, pharmacy_id=pharmacy_id)
        form = PharmacyForm(request.POST, instance=pharmacy)
        if form.is_valid():
            form.save()
            return pharmacyHome(request, pharmacy=pharmacy_id,
                message="[%s] %s profile successfully updated." % (strftime("%Y-%m-%d %H:%M:%S"), pharmacy))
        else:
            return render_to_response('erx/new_pharmacy.html',
                {'pharmacy': pharmacy, 'form': form,
                 'message': '[%s] Pharmacy %s not saved. Errors: %s' % (strftime("%Y-%m-%d %H:%M:%S"), pharmacy, form.errors)},
                context_instance=RequestContext(request))

#        else:#to do
#            if 'delete' in request.POST:
#                try:
#                    Pharmacy.objects.filter(pharmacy_id=pharmacy_id).delete()
#                    return render_to_response('erx/done.html', {'message': 'Pharmacy deleted.'},
#                        context_instance=RequestContext(request))
#                except Exception as e:
#                    return render_to_response('erx/done.html', {'message': e},
#                        context_instance=RequestContext(request))

#dispense prescriptions
def dispenseRx(request, p_id):
#TO DO
    if request.method == 'GET':
        rx = get_object_or_404(Prescription, rx_id=p_id)
        form = PrescriptionForm(instance=rx)
        fields = list(form)
        fields.pop(0)
        fields.pop(0)
        fields.pop(0)

        form2 = dict()
        form2['Patient'] = rx.patient.__unicode__()
        form2['Prescriber'] = rx.prescriber.__unicode__()
        form2['Pharmacy'] = rx.pharmacy.__unicode__()        

        RxEntryForm= inlineformset_factory(Prescription, RxEntry, can_delete=True, extra=0)
        rxforms = RxEntryForm(instance=rx)
        date_created = rx.created_date
        date_modified = rx.last_modified

        data = {'date_created': date_created, 'date_modified': date_modified,
                'form': form2,'fields': fields, 'rxform': rxforms, 'rx_id': rx.rx_id}

        return render_to_response('erx/dispense_prescription.html', data,
            context_instance=RequestContext(request))
    else:
        if request.method == 'POST':
            rx = get_object_or_404(Prescription, rx_id=p_id)
            urx = rx.dispense()
            update = urx.__dict__

            data = dict({'submitted_date': update['submitted_date'], 'status': update['status'], 'prescriber': update['prescriber_id'],
                    'pharmacy': update['pharmacy_id'], 'patient': update['patient_id']})

            form = PrescriptionForm(data, instance=urx)
            print form.is_bound

            if form.is_valid():
                form.save()
                return pharmacyHome(request, prescription=p_id,
                    message='%s Prescription successfully dispensed.' % (strftime("%Y-%m-%d %H:%M:%S")))

            else:
                print form.errors, "ERROR"
                if form.non_field_errors:
                    print form.non_field_errors
                return render_to_response('erx/done.html', {'message': 'Failed', 'errors': form.errors},
            context_instance=RequestContext(request))
#
#End of Pharmacy methods
#


#
#CRUD & Search methods for Prescription
#

#create new prescription for patient
def createPrescriptionForPatient(request, p_id):

    if request.method == "POST":
        form = PrescriptionForm(request.POST)

        if form.is_valid():
            instance=form.save()
            rxentry = RxEntryForm(request.POST, instance=instance)
            
            if rxentry.is_valid():
                rxentry.save()
                #return render_to_response('erx/done.html', {'message': "Prescription created."}, context_instance=RequestContext(request))
                return prescriberHome(request, patient=p_id, message="%s Prescription successfully created." % (strftime("%Y-%m-%d %H:%M:%S")))

            else:
                return render_to_response('erx/done.html', {'message': rxentry.errors}, context_instance=RequestContext(request))

        else:
            return render_to_response('erx/done.html', {'message': form.errors}, context_instance=RequestContext(request))

    else:
        if request.method == "GET":
            patient = Patient.objects.get(patient_id = p_id)
            prescription = Prescription(patient=patient, prescriber=patient.prescriber)
            form = PrescriptionForm(instance=prescription)
            return render_to_response('erx/new_prescription.html', {'form': form, 'rxform': RxEntryForm}, context_instance=RequestContext(request))

#create new prescription for prescriber
def createPrescriptionForPrescriber(request, p_id):

    if request.method == "POST":
        form = PrescriptionForm(request.POST)

        if form.is_valid():
            instance=form.save()
            rxentry = RxEntryForm(request.POST, instance=instance)
            
            if rxentry.is_valid():
                rxentry.save()
                return prescriberHome(request, prescriber=p_id, message="Prescription successfully created.")
#                return render_to_response('erx/done.html', {'message': "Prescription created."}, context_instance=RequestContext(request))

            else:
                return render_to_response('erx/done.html', {'message': rxentry.errors}, context_instance=RequestContext(request))

        else:
            return render_to_response('erx/done.html', {'message': form.errors}, context_instance=RequestContext(request))

    else:
        if request.method == "GET":
            prescriber = Prescriber.objects.get(prescriber_id = p_id)
            prescription = Prescription(prescriber=prescriber)
            form = PrescriptionForm(instance=prescription)
            return render_to_response('erx/new_prescription.html', {'form': form, 'rxform': RxEntryForm}, context_instance=RequestContext(request))


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


#get dispensed prescription
def getDispensedRx(request, p_id):

    if request.method == 'GET':
        rx = get_object_or_404(Prescription, rx_id=p_id)
        form = PrescriptionForm(instance=rx)
        fields = list(form)
        fields.pop(0)
        fields.pop(0)
        fields.pop(0)
        form2 = dict()
        form2['Patient'] = rx.patient.__unicode__()
        form2['Prescriber'] = rx.prescriber.__unicode__()
        form2['Pharmacy'] = rx.pharmacy.__unicode__()        

        RxEntryForm= inlineformset_factory(Prescription, RxEntry, can_delete=True, extra=0)
        rxforms = RxEntryForm(instance=rx)
        date_created = rx.created_date
        date_modified = rx.last_modified
        return render_to_response('erx/old_prescription.html', {'date_created': date_created,
                                                                'date_modified': date_modified, 'form': form2,
                                                                'fields': fields, 'rxform': rxforms},
            context_instance=RequestContext(request))


#handle prescription: GET using ID, POST, DELETE
def handlePrescription(request, rx_id):

    if request.method == 'GET':
        rx = get_object_or_404(Prescription, rx_id=rx_id)

        form = PrescriptionForm(instance=rx)
        rxforms = RxEntryForm(instance=rx)
        date_created = rx.created_date
        date_modified = rx.last_modified
        return render_to_response('erx/cur_prescription.html', {'date_created': date_created,
                                                                'date_modified': date_modified,
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
                    return prescriberHome(request, prescription=rx_id,
                        message='%s Prescription successfully updated.' %(strftime("%Y-%m-%d %H:%M:%S")))
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
                    return prescriberHome(request, prescription=rx_id,
                        message='%s Prescription deleted successfully.' % (strftime("%Y-%m-%d %H:%M:%S")))
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
