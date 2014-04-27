import unittest, sys, os, urllib2

from django.test import TestCase

from erx.forms import PrescriberForm, PatientForm, PharmacyForm
from erx.forms import PrescriptionForm, RxEntryForm, LabTestForm, LabHistoryForm, AutoRxEntryForm
from erx.forms import get_ordereditem_formset

from erx.models import Prescriber, Patient, Pharmacy, Prescription, RxEntry, LabTest, LabHistory, Drug, NDF




BASE_URL='http://127.0.0.1:8000/erx'

PRESCRIBER = {'first_name': 'TestPrescriber', 'last_name': 'TestLName',
              'street_address': 'TestPlace', 'city': 'TestCity',
              'state': 'TestState', 'zipcode': '12345', 'telephone': '000-000-0000',
              'email': 'prescriber@test.com', 'license_id': 'LicenseToTest', 'pin_code': '0000'}

PHARMACY = {'pharmacy_name': 'TestPharmacy', 'license_id': 'LicenseToTest',
            'street_address': 'TestPlace', 'city': 'TestCity',
            'state': 'TestState', 'zipcode': '12345', 'telephone': '999-999-9999',
            'email': 'pharmacy@test.com', 'license_id': 'LicenseToTest', 'pin_code': '0000'}

PATIENT = {'first_name': 'TestPrescriber', 'last_name': 'TestLName',
           'street_address': 'TestPlace', 'city': 'TestCity',
           'state': 'TestState', 'zipcode': '12345', 'telephone': '000-000-0000',
           'email': 'prescriber@test.com', 'medical_id': '000-00-0000', 'birth_date': '03/15/1890',
           'gender': 'MALE', 'weight': '180', 'height': '180', 'em_contact_name': 'EMContact', 'em_contact_phone': '000-000-0001'
}

# Create your tests here.

class PrescriberTestCase():
    """
        This class holds the unit tests for prescriber object.
    """

    def test_createPrescriber():
        """
            Test for creating a prescriber successfully.
        """

        prescriber = Prescriber(PRESCRIBER)
        
        print 'Success'


PrescriberTestCase().test_createPrescriber()
