from django import forms
from django.db import models
from django.forms import fields, models, formsets, widgets, ModelForm
from django.forms.models import inlineformset_factory

from erx.models import Prescriber, Patient, Pharmacy, Prescription, RxEntry, MedicalHistory, LabTest, LabHistory, Drug


#Prescriber form
class PrescriberForm(ModelForm):
    class Meta:
        model = Prescriber
        fields = ['first_name', 'middle_name', 'last_name', 'license_id',
                  'pin_code', 'street_address', 'city', 'state', 'zipcode',
                  'telephone', 'email']
        widgets = { 'pin_code': forms.PasswordInput(), }


#Patient form
class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['prescriber', 'medical_id', 'first_name', 'middle_name', 'last_name', 'gender',
                  'birth_date', 'food_allergy', 'current_medications', 'current_ailments', 'weight',
                  'height', 'street_address', 'city', 'state', 'zipcode', 'telephone', 'email',
                  'em_contact_name', 'em_contact_phone']

#Patient form 2
class PatientForm2(ModelForm):

    def __init__(self, prescriber=None, *args, **kwargs):
        super(PatientForm2, self).__init__(*args, **kwargs)
        if prescriber is not None:
            self.fields['prescriber'].queryset = Prescriber.objects.filter(prescriber_id = prescriber.prescriber_id)

    class Meta:
        model = Patient
        fields = ['prescriber', 'medical_id', 'first_name', 'middle_name', 'last_name', 'gender',
                  'birth_date', 'food_allergy', 'current_medications', 'current_ailments', 'weight',
                  'height', 'street_address', 'city', 'state', 'zipcode', 'telephone', 'email',
                  'em_contact_name', 'em_contact_phone']

#Pharmacy form
class PharmacyForm(ModelForm):
    class Meta:
        model = Pharmacy
        fields = ['pharmacy_name', 'license_id', 'street_address', 'city', 'state', 'zipcode', 'telephone', 'email']


#Prescription form
class PrescriptionForm(ModelForm):
    class Meta:
        model = Prescription


#Prescription form 2
class PrescriptionForm2(ModelForm):

    def __init__(self, prescriber=None, patient=None, *args, **kwargs):
        super(PrescriptionForm2, self).__init__(*args, **kwargs)

        if prescriber is not None:
            self.fields['patient'].queryset = Patient.objects.filter(prescriber=prescriber)
            self.fields['prescriber'].queryset = Prescriber.objects.filter(prescriber_id=prescriber.prescriber_id)

        if patient is not None:
            self.fields['patient'].queryset = Patient.objects.filter(patient_id=patient.patient_id)

    class Meta:
        model = Prescription



#RxEntry form
RxEntryForm = inlineformset_factory(Prescription, RxEntry, can_delete=True, extra=4)

def get_ordereditem_formset(form, formset=models.BaseInlineFormSet, **kwargs):
    return models.inlineformset_factory(Prescription, RxEntry, form, formset, **kwargs)

class AutoRxEntryForm(ModelForm):
    class Meta:
        model = RxEntry

    class Media:
        js = ('js/jquery.autocomplete.min.js', 'js/autocomplete-init.js',)
        css = {
            'all': ('css/jquery.autocomplete.css',),
        }

    def __init__(self, *args, **kwargs):
        super(AutoRxEntryForm, self).__init__(*args, **kwargs)
        self.fields['drug_name'].widget = widgets.TextInput(attrs={'class': 'autocomplete-me'})


#PatientMedicalHistory form
class MedicalHistoryForm(ModelForm):
    class Meta:
        model = MedicalHistory


#LabTest form
class LabTestForm(ModelForm):
    class Meta:
        model = LabTest


#LabHistory form
class LabHistoryForm(ModelForm):
    class Meta:
        model = LabHistory


#Drug form
class DrugForm(ModelForm):
    class Meta:
        model = Drug
