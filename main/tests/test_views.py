from django.test import TestCase
from django.core.urlresolvers import reverse
from ..models import *
from django.contrib.auth.models import User
from ..utils import fx_constants

# Create your tests here.


class AuthTestCase(TestCase):

    def setUp(self):
        self.url = reverse('login')
        user_admin = User.objects.create_user('username1', 'test@fxinterview.com', 'password')
        user_interviewer = User.objects.create_user('username2', 'test@fxinterview.com', 'password')
        user_interviewee = User.objects.create_user('username3', 'test@fxinterview.com', 'password')
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

    def test_check_user_role(self):
        self.client.login(username='username1', password='password')
        response_admin = self.client.get(reverse('main:view_home'))
        self.assertEqual(response_admin.status_code, 200)
        self.assertContains(response_admin, 'Home')

        self.client.login(username='username2', password='password')
        response_interviewer = self.client.get(reverse('main:view_home'))
        self.assertEqual(response_interviewer.status_code, 200)
        self.assertContains(response_interviewer, 'Home')

        self.client.login(username='username3', password='password')
        response_interviewee = self.client.get(reverse('main:view_home'))
        self.assertEqual(response_interviewee.status_code, 200)
        self.assertContains(response_interviewee, 'Applications')


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

    def test_start_answer(self):
        """Test """
        application_question = ApplicationQuestion.objects.get(interviewee_email='test@fxinterview.com')
        job_questions = JobQuestion.objects.filter(job=application_question.job)
        url = reverse("main:start_answer")

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

        url = reverse("main:submit_answer")

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

        url = reverse("main:submit_answer")

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

        url = reverse("main:submit_answer")

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
        url = reverse("main:finish_answer")

        resp = self.client.post(url, {'interviewee_email': application_question.interviewee_email,
                                      'application_question_id': application_question.id,
                                      'finish_action': 'submit'})

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, current_job_question.job.name)
        self.assertContains(resp, current_job_question.job.description)

        # after finish, should not show finish and submit button
        self.assertNotContains(resp, 'finish_action')
        self.assertNotContains(resp, 'submit_action')


class IntervieweeAccountTestCase(TestCase):

    def setUp(self):
        self.url = reverse('login')
        user_interviewee = User.objects.create_user('username3', 'test@fxinterview.com', 'password')
        contact_details = ContactDetails.objects.create(address1='address1', address2='address2')
        company = Company.objects.create(name='test company', contact=contact_details)
        Profile.objects.create(validated=0, role=3, contact_details=contact_details, user=user_interviewee,
                               company=company)

        job = Job.objects.create(name='test job', company=company)
        ApplicationQuestion.objects.create(interviewee_email='test@fxinterview.com',
                                           job=job, estimated_time_m=10)
        question_type = QuestionType.objects.create(type=1, display_name='General Question', description='General text question')
        question1 = Question.objects.create(name='test question1', company=company, question_type=question_type)
        question2 = Question.objects.create(name='test question2', company=company, question_type=question_type)
        JobQuestion.objects.create(job=job, question=question1)
        JobQuestion.objects.create(job=job, question=question2)

    def test_view_profile(self):
        """Test view profile page
        """
        self.client.login(username='username3', password='password')
        interviewee = User.objects.filter(username= 'username3').first()
        view_profile = self.client.get(reverse('main:view_profile'))
        self.assertEqual(view_profile.status_code, 200)
        self.assertContains(view_profile, 'First Name')
        self.assertContains(view_profile, 'Last Name')
        self.assertContains(view_profile, interviewee.username)
        self.assertContains(view_profile, interviewee.first_name)
        self.assertContains(view_profile, interviewee.last_name)
        self.assertContains(view_profile, interviewee.email)