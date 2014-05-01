from django.test import TestCase

from erx.models import Prescriber, Pharmacy, Patient, Prescription, RxEntry

class URLTestCase(TestCase):

    def test_login(self):
        response = self.client.get('/erx/login/')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get('/erx/logout/')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.get('/erx/register/')
        self.assertEqual(response.status_code, 200)

    def test_autocomplete(self):
        data = {'q': 'aspir'}
        response = self.client.get('/erx/autocomplete-drug/', data)
        self.assertEqual(response.status_code, 200)

    def test_prescriberHome(self):
        response = self.client.get('/erx/prescriber/home/')
        self.assertEqual(response.status_code, 302)

    def test_pharmacyHome(self):
        response = self.client.get('/erx/pharmacy/home/')
        self.assertEqual(response.status_code, 302)


class ModelTestCase(TestCase):

    def test_createPrescriber(self):
        Prescriber(first_name='Test', last_name='Prescriber', street_address='Test Place',
                    city='SJ', state='CA', zipcode='95101', telephone='101-101-1010', email='test@t.com',
                    license_id = 'SomeFakeLicense', pin_code='0001').save()

        pin = Prescriber.objects.get(telephone='101-101-1010').pin_code
        self.assertEqual(pin, '0001')


    def test_createPharmacy(self):
        Pharmacy(pharmacy_name='TestPharma', license_id = 'SomeFakeLicense', street_address='Test Place',
                 city='SJ', state='CA', zipcode='95101', telephone='101-101-1010', email='test@t.com').save()

        email = Pharmacy.objects.get(telephone='101-101-1010').email
        self.assertEqual(email, 'test@t.com')


    def test_createPatient(self):
        Prescriber(first_name='Test', last_name='Prescriber', street_address='Test Place',
                   city='SJ', state='CA', zipcode='95101', telephone='101-101-1010', email='test@t.com',
                   license_id = 'SomeFakeLicense', pin_code='0001').save()

        prescriber = Prescriber.objects.get(email='test@t.com')

        Patient(prescriber=prescriber, first_name='Unlucky', last_name='Patient', medical_id='123-45-6789', birth_date = '1990-03-13',
                gender='MALE', weight='100', height='100', em_contact_name='Nameless', em_contact_phone='000-000-0000',
                street_address='Test Place', city='SJ', state='CA', zipcode='95101', telephone='101-101-1010', email='test2@t.com').save()

        patient = Patient.objects.get(medical_id='123-45-6789')
        self.assertEqual(patient.email, 'test2@t.com')


    def test_createPrescription(self):
        Prescriber(first_name='Test', last_name='Prescriber', street_address='Test Place',
                   city='SJ', state='CA', zipcode='95101', telephone='101-101-1010', email='test@t.com',
                   license_id = 'SomeFakeLicense', pin_code='0001').save()

        prescriber = Prescriber.objects.get(email='test@t.com')

        Patient(prescriber=prescriber, first_name='Unlucky', last_name='Patient', medical_id='123-45-6789', birth_date = '1990-03-13',
                gender='MALE', weight='100', height='100', em_contact_name='Nameless', em_contact_phone='000-000-0000',
                street_address='Test Place', city='SJ', state='CA', zipcode='95101', telephone='101-101-1010', email='test2@t.com').save()

        Pharmacy(pharmacy_name='TestPharma', license_id = 'SomeFakeLicense', street_address='Test Place',
                 city='SJ', state='CA', zipcode='95101', telephone='101-101-1010', email='test@t.com').save()

        patient = Patient.objects.get(medical_id='123-45-6789')
        pharmacy = Pharmacy.objects.get(telephone='101-101-1010')

        Prescription(prescriber=prescriber, patient=patient, pharmacy=pharmacy,
                     note='ThisIsATestPrescription', submitted_date='2014-04-30').save()

        prescription = Prescription.objects.get(prescriber=prescriber, patient=patient, pharmacy=pharmacy)
        self.assertEqual(prescription.note, 'ThisIsATestPrescription')


    def test_dispense(self):
        Prescriber(first_name='Test', last_name='Prescriber', street_address='Test Place',
                   city='SJ', state='CA', zipcode='95101', telephone='101-101-1010', email='test@t.com',
                   license_id = 'SomeFakeLicense', pin_code='0001').save()

        prescriber = Prescriber.objects.get(email='test@t.com')

        Patient(prescriber=prescriber, first_name='Unlucky', last_name='Patient', medical_id='123-45-6789', birth_date = '1990-03-13',
                gender='MALE', weight='100', height='100', em_contact_name='Nameless', em_contact_phone='000-000-0000',
                street_address='Test Place', city='SJ', state='CA', zipcode='95101', telephone='101-101-1010', email='test2@t.com').save()

        Pharmacy(pharmacy_name='TestPharma', license_id = 'SomeFakeLicense', street_address='Test Place',
                 city='SJ', state='CA', zipcode='95101', telephone='101-101-1010', email='test@t.com').save()

        patient = Patient.objects.get(medical_id='123-45-6789')
        pharmacy = Pharmacy.objects.get(telephone='101-101-1010')

        Prescription(prescriber=prescriber, patient=patient, pharmacy=pharmacy,
                     note='ThisIsATestPrescription', submitted_date='2014-04-30').save()

        prescription = Prescription.objects.get(prescriber=prescriber, patient=patient, pharmacy=pharmacy)
        prescription.dispense().save()
        prescription = Prescription.objects.get(prescriber=prescriber, patient=patient, pharmacy=pharmacy, note='ThisIsATestPrescription')
        self.assertEqual(prescription.status, 'DISPENSED')


    def test_createRxEntry(self):
        Prescriber(first_name='Test', last_name='Prescriber', street_address='Test Place',
                   city='SJ', state='CA', zipcode='95101', telephone='101-101-1010', email='test@t.com',
                   license_id = 'SomeFakeLicense', pin_code='0001').save()

        prescriber = Prescriber.objects.get(email='test@t.com')

        Patient(prescriber=prescriber, first_name='Unlucky', last_name='Patient', medical_id='123-45-6789', birth_date = '1990-03-13',
                gender='MALE', weight='100', height='100', em_contact_name='Nameless', em_contact_phone='000-000-0000',
                street_address='Test Place', city='SJ', state='CA', zipcode='95101', telephone='101-101-1010', email='test2@t.com').save()

        Pharmacy(pharmacy_name='TestPharma', license_id = 'SomeFakeLicense', street_address='Test Place',
                 city='SJ', state='CA', zipcode='95101', telephone='101-101-1010', email='test@t.com').save()

        patient = Patient.objects.get(medical_id='123-45-6789')
        pharmacy = Pharmacy.objects.get(telephone='101-101-1010')

        Prescription(prescriber=prescriber, patient=patient, pharmacy=pharmacy,
                     note='ThisIsATestPrescription', submitted_date='2014-04-30').save()

        prescription = Prescription.objects.get(prescriber=prescriber, patient=patient, pharmacy=pharmacy)

        RxEntry(drug_name='SomeDrug', drug_form='Oral', drug_schedule='Never', drug_quantity='None',
                drug_substitution=False, prescription=prescription).save()

        RxEntry(drug_name='AnotherDrug', drug_form='Oral', drug_schedule='Never', drug_quantity='None',
                drug_substitution=False, prescription=prescription).save()

        drug_list = RxEntry.objects.filter(prescription=prescription)

        self.assertEqual(len(drug_list), 2)
        self.assertEqual(drug_list[0].drug_name, 'SomeDrug')
        self.assertEqual(drug_list[1].drug_name, 'AnotherDrug')
