import datetime

from django.test import TestCase

from main.models import *
from ..models import *


# Create your tests here.


class FXModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        contact = ContactDetails.objects.create(address1='address1', address2='address2', address3='address3',
                                      address4='address4',
                                      email='test@fxinterview.com', phone='0871234567')
        company = Company.objects.create(name='test_company', description='test description', contact=contact)
        job = Job.objects.create(name='test_job', description='test description', company=company)
        question_type = QuestionType.objects.create(type=1, display_name='General Question',
                                                    description='General text question')
        question1 = Question.objects.create(name='test_question1', company=company,
                                description='test description', estimated_time_m=10,
                                default_template='default template', question_type=question_type)
        question2 = Question.objects.create(name='test_question2', company=company, question_type=question_type)
        job_question1 = JobQuestion.objects.create(job=job, question=question1)
        job_question2 = JobQuestion.objects.create(job=job, question=question2)
        application_question = ApplicationQuestion.objects.create(interviewee_email='test@fxinterview.com',
                                                                  job=job)

    def test_model_fields(self):
        pass


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

        application_question.finish()
        self.assertTrue(application_question.is_finished())

    def test_getting_questions(self):
        """Test loading questions by application object"""
        application_question = ApplicationQuestion.objects.get(interviewee_email="test@fxinterview.com")
        job_questions = JobQuestion.objects.filter(job=application_question.job)

        self.assertEqual(job_questions[0].question.name, 'test_question1')
        self.assertEqual(job_questions[1].question.name, 'test_question2')
