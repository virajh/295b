from django.db import models
from django.forms import ModelForm

# Create your models here.

gender_choices = (
    ('Male', 'MALE'),
    ('Female', 'FEMALE'),
)

class Patient(models.Model):
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=1)
    last_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=20, choices=gender_choices)
    birth_date = models.DateField('Date of Birth')
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)    
    email = models.EmailField(max_length=200)

    def __unicode__(self):
        return self.first_name+" "+self.middle_name+" "+self.last_name

class NewPatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'


form_choices = (('Oral','ORAL'), ('Injection','INJECTION'),
    ('Drops', 'DROPS'), ('Ointment', 'OINTMENT'),
    ('Tablet', 'TABLET'), ('Capsule', 'CAPSULE'),
    ('Inhalation', 'INHALATION'),
)

class Prescription(models.Model):
    patient = models.ForeignKey(Patient)
    medicine_name = models.CharField(max_length=200)
    directions = models.CharField(max_length=200)
    form_of_administration = models.CharField(max_length=50, choices=form_choices)
    concentration = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)

class NewPrescriptionForm(ModelForm):
    class Meta:
        model = Prescription
        fields = '__all__'

