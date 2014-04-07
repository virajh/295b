from django import forms
from django.db import models
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from erx.models import Prescriber, Patient, Pharmacy, Prescription, RxEntry, PatientMedicalHistory


#Prescriber form
class PrescriberForm(ModelForm):
    class Meta:
        model = Prescriber
        fields = ['first_name', 'middle_name', 'last_name', 'license_id',
                  'pin_code', 'street_address', 'city', 'state', 'zipcode',
                  'telephone', 'email']
#        widgets = { 'pin_code': forms.PasswordInput(), }


#Patient form
class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['prescriber', 'medical_id', 'first_name', 'middle_name', 'last_name', 'gender',
                  'birth_date', 'weight', 'height', 'street_address', 'city', 'state', 'zipcode',
                  'telephone', 'email', 'em_contact_name', 'em_contact_phone']


#Pharmacy form
class PharmacyForm(ModelForm):
    class Meta:
        model = Pharmacy


#Prescription form
class PrescriptionForm(ModelForm):
    class Meta:
        model = Prescription


#ReadOnlyPrescription form
class ReadOnlyPrescriptionForm(ModelForm):

    class Meta:
        model = Prescription
        readonly_fields=['prescriber']


#PatientMedicalHistory form
class PatientMedHistForm(ModelForm):

    class Meta:
        model = PatientMedicalHistory

#RxEntry form
RxEntryForm = inlineformset_factory(Prescription, RxEntry, can_delete=True, extra=1)
