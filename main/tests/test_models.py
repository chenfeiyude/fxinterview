from django.test import TestCase

from ..models import *
from django.utils import timezone
import datetime
from ..utils import fx_timezone_utils

# Create your tests here.


class FXModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        contact = ContactDetails.objects.create(address1='address1', address2='address2', address3='address3',
                                      address4='address4',
                                      email='test@fxinterview.com', phone='0871234567')
        company = Company.objects.create(name='test_company', description='test description', contact=contact)
        job = Job.objects.create(name='test_job', description='test description', company=company)
        question1 = Question.objects.create(name='test_question1', company=company,
                                description='test description', estimated_time_m=10,
                                default_template='default template')
        question2 = Question.objects.create(name='test_question2', company=company)
        job_question1 = JobQuestion.objects.create(job=job, question=question1)
        job_question2 = JobQuestion.objects.create(job=job, question=question2)
        application_question = ApplicationQuestion.objects.create(interviewee_email='test@fxinterview.com',
                                                                  job=job)

    def test_model_fields(self):
        pass


class ContactDetailsTestCase(FXModelTestCase):

    def test_model_fields(self):
        contact_details = ContactDetails.objects.get(email='test@fxinterview.com')
        self.assertIsNotNone(contact_details)
        self.assertEqual(contact_details.address1, 'address1')
        self.assertEqual(contact_details.address2, 'address2')
        self.assertEqual(contact_details.address3, 'address3')
        self.assertEqual(contact_details.address4, 'address4')
        self.assertEqual(contact_details.email, 'test@fxinterview.com')
        self.assertEqual(contact_details.phone, '0871234567')


class CompanyTestCase(FXModelTestCase):

    def test_model_fields(self):
        contact_details = ContactDetails.objects.get(email='test@fxinterview.com')
        company = Company.objects.get(name='test_company')
        self.assertIsNotNone(company)
        self.assertEqual(company.name, 'test_company')
        self.assertEqual(company.description, 'test description')
        self.assertEqual(company.contact, contact_details)
        self.assertTrue(company.updated < timezone.now())


class JobTestCase(FXModelTestCase):

    def test_model_fields(self):
        company = Company.objects.get(name='test_company')
        job = Job.objects.get(name='test_job')

        self.assertIsNotNone(job)
        self.assertEqual(job.name, 'test_job')
        self.assertEqual(job.description, 'test description')
        self.assertEqual(job.company, company)
        self.assertTrue(job.updated < timezone.now())

    def test_get_questions(self):
        job = Job.objects.get(name='test_job')
        job_questions = job.get_questions()
        self.assertIsNotNone(job_questions)
        self.assertEqual(len(job_questions), 2)
        self.assertEqual(job_questions[0].name, 'test_question1')
        self.assertEqual(job_questions[1].name, 'test_question2')


class QuestionsTestCase(FXModelTestCase):

    def test_model_fields(self):
        company = Company.objects.get(name='test_company')
        questions = Question.objects.filter(company=company)

        self.assertIsNotNone(questions)
        self.assertEqual(len(questions), 2)
        self.assertEqual(questions[0].name, 'test_question1')
        self.assertEqual(questions[0].description, 'test description')
        self.assertEqual(questions[0].company, company)
        self.assertEqual(questions[0].estimated_time_m, 10)
        self.assertEqual(questions[0].default_template, 'default template')
        self.assertTrue(questions[0].updated < timezone.now())

        self.assertEqual(questions[1].name, 'test_question2')
        self.assertEqual(questions[1].estimated_time_m, 0)
        self.assertTrue(questions[1].updated < timezone.now())


class JobQuestionTestCase(FXModelTestCase):

    def test_model_fields(self):
        job = Job.objects.get(name='test_job')
        question = Question.objects.get(name='test_question1')
        job_question = JobQuestion.objects.get(question=question)
        self.assertIsNotNone(job_question)
        self.assertEqual(job_question.question, question)
        self.assertEqual(job_question.job, job)


class ApplicationQuestionTestCase(FXModelTestCase):

    def test_model_fields(self):
        """Test application question and other models's relationship"""
        job = Job.objects.get(name='test_job')
        application_question = ApplicationQuestion.objects.get(interviewee_email="test@fxinterview.com")

        self.assertEqual(application_question.interviewee_email, 'test@fxinterview.com')
        self.assertTrue(application_question.is_init())
        self.assertEqual(application_question.job, job)
        self.assertIsNone(application_question.deadline)
        self.assertIsNone(application_question.start_time)
        self.assertIsNone(application_question.end_time)
        self.assertEqual(application_question.estimated_time_m, 0)
        self.assertIsNone(application_question.get_estimated_end_time())

        estimated_time_m = 10
        application_question.estimated_time_m = estimated_time_m
        application_question.start()
        self.assertFalse(application_question.is_init())
        self.assertEqual(application_question.get_estimated_end_time(), application_question.start_time + datetime.timedelta(minutes=estimated_time_m))
        self.assertFalse(application_question.is_expired())

    def test_getting_questions(self):
        """Test loading questions by application object"""
        application_question = ApplicationQuestion.objects.get(interviewee_email="test@fxinterview.com")
        job_questions = JobQuestion.objects.filter(job=application_question.job)

        self.assertEqual(job_questions[0].question.name, 'test_question1')
        self.assertEqual(job_questions[1].question.name, 'test_question2')
