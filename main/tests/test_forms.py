from django.test import TestCase
from ..forms import JobForm
from ..models import *


# Create your tests here.
class JobFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        contact = ContactDetails.objects.create(address1='address1', address2='address2', address3='address3',
                                      address4='address4',
                                      email='test@fxinterview.com', phone='0871234567')
        Company.objects.create(name='test_company', description='test description', contact=contact)

    def test_forms_valid(self):
        company = Company.objects.get(name='test_company')
        valid_form_data = {'name': 'fake job 1', 'description': 'fake description 1', 'company': company.id}
        valid__form = JobForm(data=valid_form_data)
        self.assertTrue(valid__form.is_valid())

    def test_forms_invalid(self):
        in_valid_form_data = {'name': '', 'description': 'fake description 1', 'Company': '1'}
        in_valid__form = JobForm(data=in_valid_form_data)
        self.assertFalse(in_valid__form.is_valid())
