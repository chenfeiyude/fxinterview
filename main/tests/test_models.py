from django.test import TestCase

from ..models import *

# Create your tests here.


class ApplicationQuestionTestCase(TestCase):

    def setUp(self):
        ContactDetails.objects.create(address1='address1', address2='address2')
        Company.objects.create(name='test company', contact=ContactDetails.objects.get(pk=1))
        Job.objects.create(name='test job', company=Company.objects.get(pk=1))
        ApplicationQuestion.objects.create(interviewee_email='test@fxinterview.com', job=Job.objects.get(pk=1))
        Question.objects.create(name='test question1')
        Question.objects.create(name='test question2')
        JobQuestion.objects.create(job=Job.objects.get(pk=1), question=Question.objects.get(pk=1))
        JobQuestion.objects.create(job=Job.objects.get(pk=1), question=Question.objects.get(pk=2))

    def test_model_relationship(self):
        """Test application question and other models's relationship"""
        application_question = ApplicationQuestion.objects.get(interviewee_email="test@fxinterview.com")

        self.assertEqual(application_question.interviewee_email, 'test@fxinterview.com')
        self.assertEqual(application_question.job.name, 'test job')
        self.assertEqual(application_question.job.company.name, 'test company')
        self.assertEqual(application_question.job.company.contact.address1, 'address1')

        job_questions = JobQuestion.objects.filter(job=application_question.job)

        self.assertEqual(job_questions[0].question.name, 'test question1')
        self.assertEqual(job_questions[1].question.name, 'test question2')
