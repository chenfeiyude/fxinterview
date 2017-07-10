from django.test import TestCase
from django.core.urlresolvers import reverse

from ..models import *

# Create your tests here.


class ApplicationViewTestCase(TestCase):

    def setUp(self):
        ContactDetails.objects.create(address1='address1', address2='address2')
        Company.objects.create(name='test company', contact=ContactDetails.objects.get(address1='address1', address2='address2'))
        Job.objects.create(name='test job', company=Company.objects.get(name='test company'))
        ApplicationQuestion.objects.create(interviewee_email='test@fxinterview.com', job=Job.objects.get(name='test job'))
        Question.objects.create(name='test question1',  company=Company.objects.get(name='test company'))
        Question.objects.create(name='test question2',  company=Company.objects.get(name='test company'))
        JobQuestion.objects.create(job=Job.objects.get(name='test job'), question=Question.objects.get(name='test question1'))
        JobQuestion.objects.create(job=Job.objects.get(name='test job'), question=Question.objects.get(name='test question2'))

    def test_not_found(self):
        """Test if no email sent and the view return 404 not found error"""
        application_question = ApplicationQuestion.objects.get(interviewee_email='test@fxinterview.com')
        url = reverse("main:view_application_questions", kwargs={'application_question_id':application_question.id})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

    def test_found(self):
        """Test if found the application question view by sending email and application id"""
        application_question = ApplicationQuestion.objects.get(interviewee_email='test@fxinterview.com')
        url = "%s?interviewee_email=test@fxinterview.com" \
              % reverse("main:view_application_questions", kwargs={'application_question_id': application_question.id} )
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)