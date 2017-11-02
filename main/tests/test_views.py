from django.test import TestCase
from django.core.urlresolvers import reverse
from ..models import *
from job_applications.models import *
from django.contrib.auth.models import User

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