import time

from django.core.validators import RegexValidator
from django.db import models

# Create your models here.

#
#Abstract Contact Object
#
class Contact(models.Model):

    street_address = models.CharField(verbose_name='Street Address', max_length=200)
    city = models.CharField(max_length=50, default = 'San Jose')
    state = models.CharField(max_length = 200, default = 'CA')

    zipcode = models.CharField(max_length=5, validators=[RegexValidator(regex='^\d{5}$',
        message='Zipcode should be 5 digits', code='Invalid Zipcode')])

    telephone = models.CharField(max_length=12, unique=True, default = 'xxx-xxx-xxxx',
                                 validators=[RegexValidator(regex='^\d{3}-\d{3}-\d{4}$',
                                             message='Telephone number should be 10 digits xxx-xxx-xxxx',
                                             code='Invalid Telephone')])

    email = models.EmailField(max_length=200, unique=True)

    class Meta:
        abstract = True
#
#End of Contact
#


#
#Abstract Person Object
#
class Person(models.Model):

    first_name = models.CharField(verbose_name='First Name', max_length=200)
    middle_name = models.CharField(verbose_name='Middle Name', max_length=200, blank=True)
    last_name = models.CharField(verbose_name='Last Name', max_length=200)

    class Meta:
        abstract = True
#
#End of Person
#


#
#Concrete Prescriber Object
#
class Prescriber(Person, Contact):

    license_id = models.CharField(verbose_name='Authorized License ID', max_length=20)
    prescriber_id = models.AutoField(primary_key=True)
    pin_code = models.CharField(verbose_name='PIN', max_length=4,
                                validators=[RegexValidator(regex='^\d{4}$',
                                       message='Format has to be 0000',
                                       code='Invalid PIN Number')])

    def __unicode__(self):
        if self.middle_name:
            return self.first_name+" "+self.middle_name+" "+self.last_name
        else:
            return self.first_name+" "+self.last_name
#
#End of Prescriber
#


#
#Patient Object
#
gender_choices = (
    ('Male', 'MALE'),
    ('Female', 'FEMALE'),
)

class Patient(Person, Contact):

    date_added = models.DateTimeField(auto_now_add = True)
    prescriber = models.ForeignKey(Prescriber)
    patient_id = models.AutoField(primary_key=True)
    medical_id = models.CharField(verbose_name='Medical ID', unique=True, max_length=11,
                           validators=[RegexValidator(regex='^\d{3}-\d{2}-\d{4}$',
                                       message='Format has to be 123-45-6789',
                                       code='Invalid Medical ID')],
          default='xxx-xx-xxxx')

    birth_date = models.DateField(verbose_name='Date of Birth ', default='mm/dd/yyyy')
    gender = models.CharField(verbose_name='Gender', max_length=20, choices=gender_choices)

    food_allergy = models.CharField(verbose_name='Known Food Allergies', max_length=4000, help_text='Enter CSV values', blank=True)
    current_medications = models.CharField(verbose_name='Current Medications', max_length=4000, help_text='Enter CSV values', blank=True)
    current_ailments = models.CharField(verbose_name='Current Ailments diagnosed', max_length=4000, blank=True)
    weight = models.CharField(verbose_name='Weight (in lbs)', max_length=20)
    height = models.CharField(verbose_name='Height (in cm)', max_length=20) 

    em_contact_name = models.CharField(verbose_name='Emergency Contact Name', max_length=100)
    em_contact_phone = models.CharField(verbose_name='Emergency Contact Telephone', max_length=12, unique=True, default = 'xxx-xxx-xxxx',
                                 validators=[RegexValidator(regex='^\d{3}-\d{3}-\d{4}$',
                                             message='Telephone number should be 10 digits xxx-xxx-xxxx',
                                             code='Invalid Telephone')])

    def __unicode__(self):
        if self.middle_name:
            return self.first_name+" "+self.middle_name+" "+self.last_name+" (" + self.medical_id + ")"
        else:
            return self.first_name+" "+self.last_name+" ("+self.medical_id+ ")"
#
#End of Patient
#


#
#Pharmacy Object
#
class Pharmacy(Contact):

    pharmacy_name = models.CharField(verbose_name='Pharmacy Name', max_length=200)
    pharmacy_id = models.AutoField(primary_key=True)

    license_id = models.CharField(verbose_name='Pharmacy License ID', max_length=11,
                           validators=[RegexValidator(regex='^\d{3}-\d{2}-\d{4}$',
                                       message='Format has to be 123-45-6789',
                                       code='Invalid License ID')],
          default='xxx-xx-xxxx')

    def __unicode__(self):
        return self.pharmacy_name
#
#End of Pharmacy
#


#
#Prescription Object
#
st_choices = (
    ('PENDING', 'Pending'),
    ('SUBMITTED', 'Submitted'),
    ('DISPENSED', 'Dispensed'),
)

class Prescription(models.Model):

    rx_id = models.AutoField(primary_key=True)

    prescriber = models.ForeignKey(Prescriber)
    patient = models.ForeignKey(Patient)
    pharmacy = models.ForeignKey(Pharmacy)

    sp_instructions = models.CharField(verbose_name='Special Instructions', default='Stop in 3 weeks.', max_length=2000, blank=True)
    note = models.CharField(verbose_name='Note to Pharmacy', max_length=2000, default='Check ID.', blank=True)

    created_date = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now=True)
    submitted_date = models.DateField(verbose_name='Date of Submission', default=time.strftime("%m/%d/%Y"))

    status = models.CharField('Status', max_length=20, choices=st_choices, default='PENDING')

    def __unicode__(self):
        return "%s %s: %s "%(self.created_date.date(), self.prescriber, self.patient)

    def dispense(self):
        self.status = st_choices[2][0]
        return self

#
#End of Prescription
#


#
#RxEntry Object
#
refill_choices = (
    (0,0),
    (1,1),
    (2,2),
    (3,3),
)

form_choices = (
    ('Chewable Tablet', 'Chewable Tablet'),
    ('Oral Tablet', 'Oral Tablet'),
    ('Oral Pill', 'Oral Pill'),
    ('Intravenous Injection', 'Intravenous Injection'),
    ('Oral Solution', 'Oral Solution'),
    ('Oral Capsule', 'Oral Capsule'),
    ('Topical Cream', 'Topical Cream'),
    ('Extended Release Tablet', 'Extended Release Tablet'),
    ('Oral Syrup', 'Oral Syrup'),
    ('Nasal Spray', 'Nasal Spray'),
)

class RxEntry(models.Model):

    drug_name = models.CharField(verbose_name='Drug & Concentration', max_length=200)
    drug_form = models.CharField(verbose_name='Drug Form', max_length=50)
    drug_schedule = models.CharField(verbose_name='Dosage Instructions', max_length=2000)    
    drug_quantity = models.CharField(verbose_name='Dosage Amount', max_length=2000)
    drug_substitution = models.BooleanField(verbose_name='Substitution allowed?')
    refills = models.IntegerField('Number of Refills', max_length=5, choices=refill_choices, default=0)
    prescription = models.ForeignKey(Prescription)

    def __unicode__(self):
        return "%s\n%s\n%s\n" % (self.drug_name, self.drug_schedule, self.drug_quantity)

#
#End of RxEntry
#

#
#Helper classes for Drug-Drug Interactions
#
class NDF(models.Model):
    drug_id = models.AutoField(primary_key=True)
    nui = models.CharField(verbose_name='NUI', max_length=50, unique=True)
    data = models.CharField(verbose_name='Data', max_length=200, unique=True)

    def __unicode__(self):
        return self.data

    def getID(self):
        return self.nui

class Drug(models.Model):
    drug_id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='Name', max_length=200, unique=True)

    def __unicode__(self):
        return self.name

    def __init__(self, **kwargs):
        super(Drug, self).__init__()
        if 'name' in kwargs:
            self.name = kwargs['name']

#
#End of helper classes
#

#
#Lab Test Object
#
class LabTest(models.Model):

    lab_history = models.ForeignKey('LabHistory')
    test_name = models.CharField(verbose_name='Test Name', max_length=200)
    test_result = models.CharField(verbose_name='Test Result', max_length=2000)
    normal_range = models.CharField(verbose_name='Normal Range', max_length=2000)
    units = models.CharField(verbose_name='Units', max_length=200)
#
#End of Lab Test 
#


#
#Lab History Object
#
class LabHistory(models.Model):

    test_id = models.CharField(verbose_name='Test ID', max_length=200)
    patient = models.ForeignKey('Patient')
    prescriber = models.ForeignKey('Prescriber')
    test_date = models.DateField(verbose_name='Date of Test', default='mm/dd/yyyy')
    pmh = models.ForeignKey('MedicalHistory')

#
#End of Lab History
#


#
#Patient Medical History Object
#
class MedicalHistory(models.Model):

    patient = models.OneToOneField(Patient)
#    food_allergy = models.CharField(verbose_name='Known Food Allergies', max_length=4000, default='Enter CSV values')
#    current_medications = models.CharField(verbose_name='Current Medications', max_length=4000, default='Enter CSV values')
#    current_ailments = models.CharField(verbose_name='Current Ailments diagnosed', max_length=4000, default='Enter CSV values')
    
#
#End of Patient Medical History
#
"""
#
#RxNorm drug database
#
class Rxnconso(models.Model):
    rxcui = models.CharField(db_column='RXCUI', max_length=8) # Field name made lowercase.
    lat = models.CharField(db_column='LAT', max_length=3) # Field name made lowercase.
    ts = models.CharField(db_column='TS', max_length=1, blank=True) # Field name made lowercase.
    lui = models.CharField(db_column='LUI', max_length=8, blank=True) # Field name made lowercase.
    stt = models.CharField(db_column='STT', max_length=3, blank=True) # Field name made lowercase.
    sui = models.CharField(db_column='SUI', max_length=8, blank=True) # Field name made lowercase.
    ispref = models.CharField(db_column='ISPREF', max_length=1, blank=True) # Field name made lowercase.
    rxaui = models.CharField(db_column='RXAUI', max_length=8, primary_key=True) # Field name made lowercase.
    saui = models.CharField(db_column='SAUI', max_length=50, blank=True) # Field name made lowercase.
    scui = models.CharField(db_column='SCUI', max_length=50, blank=True) # Field name made lowercase.
    sdui = models.CharField(db_column='SDUI', max_length=50, blank=True) # Field name made lowercase.
    sab = models.CharField(db_column='SAB', max_length=20) # Field name made lowercase.
    tty = models.CharField(db_column='TTY', max_length=20) # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=50) # Field name made lowercase.
    str = models.CharField(db_column='STR', max_length=3000) # Field name made lowercase.
    srl = models.CharField(db_column='SRL', max_length=10, blank=True) # Field name made lowercase.
    suppress = models.CharField(db_column='SUPPRESS', max_length=1, blank=True) # Field name made lowercase.
    cvf = models.CharField(db_column='CVF', max_length=50, blank=True) # Field name made lowercase.
    refills = models.IntegerField('Number of Refills', max_length=5, choices=refill_choices, default=0)
    class Meta:
        db_table = 'RXNCONSO'

    def __unicode__(self):
        return self.str

    def getDrug(self):
        return self.str
#
#End of Rxconso
#


gender_choices = (
    ('Male', 'MALE'),
    ('Female', 'FEMALE'),
)

class Patient(models.Model):
    first_name = models.CharField(verbose_name='First Name', max_length=200)
    middle_name = models.CharField(verbose_name='Middle Name', max_length=200, blank=True)
    last_name = models.CharField(verbose_name='Last Name', max_length=200)

    uid = models.CharField(verbose_name='Medical ID', primary_key=True, max_length=11,
        validators=[RegexValidator(regex='^\d{3}-\d{2}-\d{4}$',
            message='Format has to be 123-45-6789',
            code='Invalid Medical ID')],
        default='xxx-xx-xxxx')

    birth_date = models.DateField(verbose_name='Date of Birth ', default='mm/dd/yyyy')
    gender = models.CharField(verbose_name='Gender', max_length=20, choices=gender_choices)
    weight = models.CharField(verbose_name='Weight (in lbs)', max_length=20)
    height = models.CharField(verbose_name='Height (in cm)', max_length=20) 
    date_added = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        if len(self.middle_name) >= 1:
            return self.first_name+" "+self.middle_name+" "+self.last_name+" "+self.uid
        else:
            return self.first_name+" "+self.last_name+" "+self.uid

class PatientForm(ModelForm):
    class Meta:
       model = Patient
#
#End of Patient
#

#
#Contact information is separate object
#
class Contact(models.Model):
    
    uid = models.CharField(verbose_name='Medical ID', primary_key=True, max_length=11,
        validators=[RegexValidator(regex='^\d{3}-\d{2}-\d{4}$',
            message='Format has to be 123-45-6789',
            code='Invalid Medical ID')],
        default='xxx-xx-xxxx')

    street_address = models.CharField(verbose_name='Street Address', max_length=200)
    house_number = models.CharField(verbose_name='House/Apt. No', max_length=10, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length = 200)
    zipcode = models.CharField(max_length=5, validators=[RegexValidator(regex='^\d{5}$',
        message='Zipcode should be 5 digits', code='Invalid Zipcode')])

    telephone = models.CharField(max_length=12, unique=True, validators=[RegexValidator(regex='^\d{3}-\d{3}-\d{4}$',
        message='Telephone number should be 10 digits xxx-xxx-xxxx', code='Invalid Telephone')])
    
    email = models.EmailField(max_length=200, unique=True)

    def __unicode__(self):
        return self.uid+" "+self.street_address+" "+self.house_number


class ContactForm(ModelForm):
    class Meta:
        model = Contact
#
#End of Contact
#

#
#NewPatient inherits Patient and Contact class
#
class NewPatient(Patient, Contact):

    def __unicode__(self):
        super()

class NewPatientForm(ModelForm):
    class Meta:
        model = NewPatient
#last_modified = models.DateTimeField(auto_now=True)
#End of NewPatient
#


#
#Pharmacy Object
#
class Pharmacy(models.Model):

    pharmacy_name = models.CharField(verbose_name='Pharmacy Name', max_length=200)

    uid = models.CharField(verbose_name='Pharmacy ID', primary_key=True, max_length=11,
        validators=[RegexValidator(regex='^\d{3}-\d{2}-\d{4}$',
            message='Format has to be 123-45-6789',
            code='Invalid Pharmacy ID')],
        default='xxx-xx-xxxx')

    def __unicode__(self):
        return self.pharmacy_name + " " + self.uid

class PharmacyForm(ModelForm):
    class Meta:
        model = Pharmacy
#
#End of Pharmacy
#

#
#NewPharmacy Object
#
class NewPharmacy(Pharmacy, Contact):

    def __unicode__(self):
        super()

class NewPharmacyForm(ModelForm):
    class Meta:
        model = NewPharmacy
#
#End of NewPharmacy
#

#
#Medicine Object to be embedded in Prescription
#
sub_choices = (
    ('YES', 'Yes'),
    ('NO', 'No'),
)

class Medicine(models.Model):
    name = models.CharField('Name', max_length=3000)
    form = models.CharField('Form', max_length=200)
    frequency = models.CharField('Frequency', max_length=1000)
    quantity = models.CharField('Dispense Quantity', max_length=20)
    instruction = models.CharField('Instructions', max_length=3000)
    substitution = models.CharField('Substitution allowed', max_length=20, choices=sub_choices)
#
#End of Medicine
#

#
#Prescription Object
#
st_choices = (
    ('PENDING', 'Pending'),
    ('SUBMITTED', 'Submitted'),
)

refill_choices = (
    (0,0),
    (1,1),
    (2,2),
    (3,3),
    (4,4),
)

class Prescription(models.Model):

    p_id = models.AutoField('Prescription ID', primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    status = models.CharField('Status', max_length=20, choices=st_choices)
    patient = models.OneToOneField(Patient)
    pharmacy = models.OneToOneField(Pharmacy)
    refills = models.IntegerField('Number of Refills', max_length=5, choices=refill_choices, default=0)
    drugs = EmbeddedModelField('Medicine')

class PrescriptionForm(ModelForm):
    class Meta:
        model = Prescription
#
#End of prescription object
#


#
#Abstract User Object
#
class User(models.Model):
    user_name = models.CharField(verbose_name='User Name', max_length=20)
    password = models.CharField(verbose_name='Password', max_length=20)
    security_question = models.CharField(verbose_name='Security Question', max_length=200)
    security_answer = models.CharField(verbose_name='Security Answer', max_length=200)

#    class Meta:
#        abstract = True

class UserForm(ModelForm):
    class Meta:
        model = User
        widgets = { 'password': forms.PasswordInput(), }
#
#End of User
#
"""
