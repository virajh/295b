from django import forms
from django.db import models
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from erx.models import Prescriber, Patient, Pharmacy, Prescription, RxEntry


#Prescriber form
class PrescriberForm(ModelForm):
    class Meta:
        model = Prescriber
        widgets = { 'pin_code': forms.PasswordInput(), }


#Patient form
class PatientForm(ModelForm):
    class Meta:
        model = Patient


#Pharmacy form
class PharmacyForm(ModelForm):
    class Meta:
        model = Pharmacy


#Prescription form
class PrescriptionForm(ModelForm):
    class Meta:
        model = Prescription

#RxEntry form
RxEntryForm = inlineformset_factory(Prescription, RxEntry, can_delete=True, extra=1)
