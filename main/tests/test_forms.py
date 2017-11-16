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
        company = Company.objects.create(name='test_company', description='test description', contact=contact)
        question_type = QuestionType.objects.create(type=1, display_name='General Question', description='General text question')
        Question.objects.create(name='test_question2', company=company, estimated_time_m=12, question_type=question_type)

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
        question = Question.objects.get(name='test_question2')
        valid_form_data = {'name': 'test_question5', 'company': company.id, 'estimated_time_m': question.estimated_time_m,
                           'question_type': question.question_type.id}
        valid__form = QuestionForm(data=valid_form_data)
        self.assertTrue(valid__form.is_valid())

    def test_question_forms_invalid(self):
        in_valid_form_data = {'name': '', 'description': 'fake description 1', 'company': '1', 'question_type': '3'}
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
