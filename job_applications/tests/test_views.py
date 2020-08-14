from django.core.urlresolvers import reverse
from django.test import TestCase

from main.models import *
from ..models import *


# Create your tests here.


class ApplicationViewTestCase(TestCase):

    def setUp(self):
        contact_details = ContactDetails.objects.create(address1='address1', address2='address2')
        company = Company.objects.create(name='test company', contact=contact_details)

        job = Job.objects.create(name='test job', company=company)
        ApplicationQuestion.objects.create(interviewee_email='test@fxinterview.com',
                                           job=job, estimated_time_m=10)
        question_type = QuestionType.objects.create(type=1, display_name='General Question',
                                                    description='General text question')
        question1 = Question.objects.create(name='test question1', company=company, question_type=question_type)
        question2 = Question.objects.create(name='test question2', company=company, question_type=question_type)
        JobQuestion.objects.create(job=job, question=question1)
        JobQuestion.objects.create(job=job, question=question2)
        
    def test_not_found_application(self):
        """Test if no email sent and the view return 404 not found error"""
        application_question = ApplicationQuestion.objects.get(interviewee_email='test@fxinterview.com')
        url = reverse("job_applications:view_application_questions", kwargs={'application_question_id':application_question.id})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

    def test_found_application(self):
        """Test if found the application question view by sending email and application id"""
        application_question = ApplicationQuestion.objects.get(interviewee_email='test@fxinterview.com')
        self.assertEqual(application_question.interviewee_email, 'test@fxinterview.com')
        url = "%s?interviewee_email=%s"\
              % (reverse("job_applications:view_application_questions", kwargs={'application_question_id': application_question.id} )
                 ,application_question.interviewee_email)
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_start_answer(self):
        """Test """
        application_question = ApplicationQuestion.objects.get(interviewee_email='test@fxinterview.com')
        job_questions = JobQuestion.objects.filter(job=application_question.job)
        url = reverse("job_applications:start_answer")

        current_job_question = job_questions[0]

        resp = self.client.post(url, {'interviewee_email': application_question.interviewee_email,
                                      'application_question_id': application_question.id,
                                      'start_action': 'submit'})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, current_job_question.job.name)
        self.assertContains(resp, current_job_question.job.description)

    def test_submit_answer(self):
        """Test submit answer succeed, and response html content should contain the submit answer"""
        application_question = ApplicationQuestion.objects.get(interviewee_email='test@fxinterview.com')
        application_question.start_time = timezone.now()
        application_question.save()

        job_questions = JobQuestion.objects.filter(job=application_question.job)

        self.assertEqual(len(job_questions), 2)

        url = reverse("job_applications:submit_answer")

        current_job_question = job_questions[0]
        answer_content = 'fake answer content'
        selected_language = fx_constants.LANGUAGE_PYTHON
        resp = self.client.post(url, {'interviewee_email': application_question.interviewee_email,
                                      'application_question_id': application_question.id,
                                      'job_question_id': current_job_question.id,
                                      'answer_content': answer_content,
                                      'selected_language': selected_language,
                                      'submit_action': 'submit'})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, answer_content)

    def test_next_question(self):
        """Test clicking next question button and it should redirect to next question gui
        1. If it has next question, then return next question
        2. If it does not have next question, then return current question
        """
        application_question = ApplicationQuestion.objects.get(interviewee_email='test@fxinterview.com')
        application_question.start_time = timezone.now()
        application_question.save()

        job_questions = JobQuestion.objects.filter(job=application_question.job)

        self.assertEqual(len(job_questions), 2)

        url = reverse("job_applications:submit_answer")

        current_job_question = job_questions[0]
        next_job_question = job_questions[1]
        selected_language = fx_constants.LANGUAGE_PYTHON

        resp = self.client.post(url, {'interviewee_email': application_question.interviewee_email,
                                      'application_question_id': application_question.id,
                                      'job_question_id': current_job_question.id,
                                      'selected_language': selected_language,
                                      'submit_action': 'next'})

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, next_job_question.job.name)
        self.assertContains(resp, next_job_question.job.description)

        current_job_question = job_questions[1]

        resp = self.client.post(url, {'interviewee_email': application_question.interviewee_email,
                                      'application_question_id': application_question.id,
                                      'job_question_id': current_job_question.id,
                                      'selected_language': selected_language,
                                      'submit_action': 'next'})

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, current_job_question.job.name)
        self.assertContains(resp, current_job_question.job.description)

    def test_prev_question(self):
        """Test clicking prev question button and it should redirect to prev question gui
        1. If it has prev question, then return prev question
        2. If it does not have prev question, then return current question
        """
        application_question = ApplicationQuestion.objects.get(interviewee_email='test@fxinterview.com')
        application_question.start_time = timezone.now()
        application_question.save()

        job_questions = JobQuestion.objects.filter(job=application_question.job)

        self.assertEqual(len(job_questions), 2)

        url = reverse("job_applications:submit_answer")

        current_job_question = job_questions[1]
        prev_job_question = job_questions[0]

        selected_language = fx_constants.LANGUAGE_PYTHON

        resp = self.client.post(url, {'interviewee_email': application_question.interviewee_email,
                                      'application_question_id': application_question.id,
                                      'job_question_id': current_job_question.id,
                                      'selected_language': selected_language,
                                      'submit_action': 'prev'})

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, prev_job_question.job.name)
        self.assertContains(resp, prev_job_question.job.description)

        current_job_question = job_questions[0]

        resp = self.client.post(url, {'interviewee_email': application_question.interviewee_email,
                                      'application_question_id': application_question.id,
                                      'job_question_id': current_job_question.id,
                                      'selected_language': selected_language,
                                      'submit_action': 'prev'})

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, current_job_question.job.name)
        self.assertContains(resp, current_job_question.job.description)

    def test_finish_answer(self):
        """Test clicking finish answer button and it should update application status to finished and redirect to
           view application page
        """
        application_question = ApplicationQuestion.objects.get(interviewee_email='test@fxinterview.com')
        application_question.start_time = timezone.now()
        application_question.save()
        job_questions = JobQuestion.objects.filter(job=application_question.job)
        current_job_question = job_questions[0]
        url = reverse("job_applications:finish_answer")

        resp = self.client.post(url, {'interviewee_email': application_question.interviewee_email,
                                      'application_question_id': application_question.id,
                                      'finish_action': 'submit'})

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, current_job_question.job.name)
        self.assertContains(resp, current_job_question.job.description)

        # after finish, should not show finish and submit button
        self.assertNotContains(resp, 'finish_action')
        self.assertNotContains(resp, 'submit_action')

