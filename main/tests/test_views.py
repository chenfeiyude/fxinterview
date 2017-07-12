import logging
from django.test import TestCase
from django.core.urlresolvers import reverse
from ..models import *
from django.contrib.auth.models import User

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

        answer_content = 'fake answer content'
        resp = self.client.post(url, {'interviewee_email':application_question.interviewee_email,
                                      'application_question_id':application_question.id,
                                      'job_question_id':job_questions[0].id,
                                      'answer_content':answer_content})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, answer_content)


class AuthTestCase(TestCase):

    def setUp(self):
        self.url = reverse("main:login")
        user_admin = User.objects.create_user('username1', 'test@gmail.com', 'password')
        user_interviewer = User.objects.create_user('username2', 'test@gmail.com', 'password')
        user_interviewee = User.objects.create_user('username3', 'test@gmail.com', 'password')
        contact_details = ContactDetails.objects.create(address1='address1', address2='address2')
        company = Company.objects.create(name='test company', contact=contact_details)
        Profile.objects.create(validated=0, role=1, contact_details=contact_details, user=user_admin, company=company)
        Profile.objects.create(validated=0, role=2, contact_details=contact_details, user=user_interviewer, company=company)
        Profile.objects.create(validated=0, role=3, contact_details=contact_details, user=user_interviewee, company=company)


    def test_check_user_login(self):
        self.assertTrue(self.client.login(username='username1', password='password'))
        self.assertFalse(self.client.login(username='wrong', password='password'))


    def test_login_refirect(self):
        resp_admin = self.client.post(self.url, {'username': 'username1', 'password': 'password'})
        self.assertRedirects(resp_admin, expected_url=reverse('main:view_home'), status_code=302, target_status_code=200)


    def test_check_ueser_role(self):
        self.client.login(username='username1', password='password')
        response_admin = self.client.get(reverse('main:view_home'))
        self.assertEqual(response_admin.status_code, 200)
        self.assertContains(response_admin, 'Admin home page')

        self.client.login(username='username2', password='password')
        response_interviewer = self.client.get(reverse('main:view_home'))
        self.assertEqual(response_interviewer.status_code, 200)
        self.assertContains(response_interviewer, 'Interviewer home page')

        self.client.login(username='username3', password='password')
        response_interviewee = self.client.get(reverse('main:view_home'))
        self.assertEqual(response_interviewee.status_code, 200)
        self.assertContains(response_interviewee, 'Interviewee home page')
