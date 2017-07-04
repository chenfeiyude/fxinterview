from django.test import TestCase

from .models import *

# Create your tests here.


class ApplicationQuestionTest(TestCase):
    def setUp(self):
        ContactDetails.objects.create(address1='address1', address2='address2')
        Company.objects.create(name='test company', contact=ContactDetails.objects.get(pk=1))
        Job.objects.create(name='test job', company=Company.objects.get(pk=1))
        ApplicationQuestion.objects.create(interviewee_email="test@fxinterview.com", job=Job.objects.get(pk=1))

    def test_animals_can_speak(self):
        """Test application question"""
        application_question = ApplicationQuestion.objects.get(interviewee_email="test@fxinterview.com")

        self.assertEqual(application_question.interviewee_email, 'test@fxinterview.com')