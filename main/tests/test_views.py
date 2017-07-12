import logging
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

    def test_not_found_application(self):
        """Test if no email sent and the view return 404 not found error"""
        application_question = ApplicationQuestion.objects.get(interviewee_email='test@fxinterview.com')
        url = reverse("main:view_application_questions", kwargs={'application_question_id':application_question.id})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

    def test_found_application(self):
        """Test if found the application question view by sending email and application id"""
        application_question = ApplicationQuestion.objects.get(interviewee_email='test@fxinterview.com')
        self.assertEqual(application_question.interviewee_email, 'test@fxinterview.com')
        url = "%s?interviewee_email=%s"\
              % (reverse("main:view_application_questions", kwargs={'application_question_id': application_question.id} )
                 ,application_question.interviewee_email)
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_submit_answer(self):
        """Test submit answer succeed, and response html content should contain the submit answer"""
        application_question = ApplicationQuestion.objects.get(interviewee_email='test@fxinterview.com')
        job_questions = JobQuestion.objects.filter(job=application_question.job)

        self.assertEqual(len(job_questions), 2)

        url = reverse("main:submit_answer")

        current_job_question = job_questions[0]
        answer_content = 'fake answer content'
        resp = self.client.post(url, {'interviewee_email': application_question.interviewee_email,
                                      'application_question_id': application_question.id,
                                      'job_question_id': current_job_question.id,
                                      'answer_content': answer_content,
                                      'submit_action': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, answer_content)
        self.assertContains(resp, current_job_question.job.name)
        self.assertContains(resp, current_job_question.job.description)

    def test_next_question(self):
        """Test clicking next question button and it should redirect to next question gui
        1. If it has next question, then return next question
        2. If it does not have next question, then return current question
        """
        application_question = ApplicationQuestion.objects.get(interviewee_email='test@fxinterview.com')
        job_questions = JobQuestion.objects.filter(job=application_question.job)

        self.assertEqual(len(job_questions), 2)

        url = reverse("main:submit_answer")

        current_job_question = job_questions[0]
        next_job_question = job_questions[1]

        resp = self.client.post(url, {'interviewee_email': application_question.interviewee_email,
                                      'application_question_id': application_question.id,
                                      'job_question_id': current_job_question.id,
                                      'next_action': ''})

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, next_job_question.job.name)
        self.assertContains(resp, next_job_question.job.description)

        current_job_question = job_questions[1]

        resp = self.client.post(url, {'interviewee_email': application_question.interviewee_email,
                                      'application_question_id': application_question.id,
                                      'job_question_id': current_job_question.id,
                                      'next_action': ''})

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, current_job_question.job.name)
        self.assertContains(resp, current_job_question.job.description)

    def test_prev_question(self):
        """Test clicking prev question button and it should redirect to prev question gui
        1. If it has prev question, then return prev question
        2. If it does not have prev question, then return current question
        """
        application_question = ApplicationQuestion.objects.get(interviewee_email='test@fxinterview.com')
        job_questions = JobQuestion.objects.filter(job=application_question.job)

        self.assertEqual(len(job_questions), 2)

        url = reverse("main:submit_answer")

        current_job_question = job_questions[1]
        prev_job_question = job_questions[0]

        resp = self.client.post(url, {'interviewee_email': application_question.interviewee_email,
                                      'application_question_id': application_question.id,
                                      'job_question_id': current_job_question.id,
                                      'prev_action': ''})

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, prev_job_question.job.name)
        self.assertContains(resp, prev_job_question.job.description)

        current_job_question = job_questions[0]

        resp = self.client.post(url, {'interviewee_email': application_question.interviewee_email,
                                      'application_question_id': application_question.id,
                                      'job_question_id': current_job_question.id,
                                      'prev_action': ''})

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, current_job_question.job.name)
        self.assertContains(resp, current_job_question.job.description)