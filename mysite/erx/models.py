from django.db import models
from django.forms import ModelForm
from django.core.validators import RegexValidator

# Create your models here.

#
#Patient information table
#
gender_choices = (
    ('Male', 'MALE'),
    ('Female', 'FEMALE'),
)

class Patient(models.Model):
    first_name = models.CharField(verbose_name='First Name', max_length=200)
    middle_name = models.CharField(verbose_name='Middle Name', max_length=200, blank=True)
    last_name = models.CharField(verbose_name='Last Name', max_length=200)

    medical_id = models.CharField(verbose_name='Medical ID', primary_key=True, max_length=11,
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
            return self.first_name+" "+self.middle_name+" "+self.last_name+" "+self.medical_id
        else:
            return self.first_name+" "+self.last_name+" "+self.medical_id

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
    
    medical_id = models.CharField(verbose_name='Medical ID', primary_key=True, max_length=11,
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

    telephone = models.CharField(max_length=12, validators=[RegexValidator(regex='^\d{3}-\d{3}-\d{4}$',
        message='Telephone number should be 10 digits xxx-xxx-xxxx', code='Invalid Telephone')])
    
    email = models.EmailField(max_length=200)

    def __unicode__(self):
        return self.medical_id+" "+self.street_address+" "+self.house_number


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
#
#End of NewPatient
#


#
#Pharmacy Object
#
class Pharmacy(models.Model):

    pharmacy_name = models.CharField(verbose_name='Pharmacy Name', max_length=200)

    medical_id = models.CharField(verbose_name='Pharmacy ID', primary_key=True, max_length=11,
        validators=[RegexValidator(regex='^\d{3}-\d{2}-\d{4}$',
            message='Format has to be 123-45-6789',
            code='Invalid Pharmacy ID')],
        default='xxx-xx-xxxx')

    def __unicode__(self):
        return self.pharmacy_name

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

    class Meta:
        db_table = 'RXNCONSO'

    def __unicode__(self):
        return self.str

    def getDrug(self):
        return self.str
#
#End of Rxconso
#
