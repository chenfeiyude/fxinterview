from django.test import TestCase
from ..forms import JobForm, QuestionForm, FXUpdateUserForm
from ..models import *


# Create your tests here.
class FormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        contact = ContactDetails.objects.create(address1='address1', address2='address2', address3='address3',
                                      address4='address4',
                                      email='test@fxinterview.com', phone='0871234567')
        Company.objects.create(name='test_company', description='test description', contact=contact)

    def test_job_forms_valid(self):
        company = Company.objects.get(name='test_company')
        valid_form_data = {'name': 'fake job 1', 'description': 'fake description 1', 'company': company.id}
        valid__form = JobForm(data=valid_form_data)
        self.assertTrue(valid__form.is_valid())

    def test_job_forms_invalid(self):
        in_valid_form_data = {'name': '', 'description': 'fake description 1', 'company': '1'}
        in_valid__form = JobForm(data=in_valid_form_data)
        self.assertFalse(in_valid__form.is_valid())

    def test_question_forms_valid(self):
        company = Company.objects.get(name='test_company')
        valid_form_data = {'name': 'fake job 1', 'description': 'fake description 1', 'company': company.id}
        valid__form = QuestionForm(data=valid_form_data)
        self.assertTrue(valid__form.is_valid())

    def test_question_forms_invalid(self):
        in_valid_form_data = {'name': '', 'description': 'fake description 1', 'company': '1'}
        in_valid__form = QuestionForm(data=in_valid_form_data)
        self.assertFalse(in_valid__form.is_valid())

    def test_update_form_valid(self):
        form_data = {'username': 'test@fxinterview.com',
                           'first_name': 'fake first name',
                           'last_name': 'fake last name',
                           'email': 'test@fxinterview.com'}
        form = FXUpdateUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_update_form_invalid(self):
        form_data = {'username': '',
                           'first_name': 'fake first name',
                           'last_name': 'fake last name',
                           'email': 'test@fxinterview.com'}
        form = FXUpdateUserForm(data=form_data)
        self.assertFalse(form.is_valid())
