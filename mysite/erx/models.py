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
    address_line_2 = models.CharField(max_length=200, blank=True)
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
#        managed = False
        db_table = 'RXNCONSO'

    def __unicode__(self):
        return self.str




class Prescription(models.Model):
    patient = models.ForeignKey(Patient)
#    medicines = models.ManyToManyField(Rxnconso)
    date = models.DateTimeField(auto_now_add=True)

class NewPrescriptionForm(ModelForm):
    class Meta:
        model = Prescription
        fields = '__all__'
