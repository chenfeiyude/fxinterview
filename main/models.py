from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ContactDetails(models.Model):
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    address3 = models.CharField(max_length=100, null=True, blank=True)
    address4 = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)


class Profile(models.Model):
    ADMIN_ROLE = 1
    INTERVIEWER_STATUS = 2
    INTERVIEWEE_STATUS = 3
    ROLE_CHOICES = (
        (ADMIN_ROLE, 'admin'),
        (INTERVIEWER_STATUS, 'interviewer'),
        (INTERVIEWEE_STATUS, 'interviewee'),
    )
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    contact_details = models.ForeignKey(ContactDetails)
    validated = models.BooleanField(default=False)
    role = models.IntegerField(choices=ROLE_CHOICES, default=ADMIN_ROLE)

    def is_role(self, check_role):
        return self.role == check_role

    def is_interviewer(self):
        return self.is_role(self.INTERVIEWER_STATUS)

    def is_interviewee(self):
        return self.is_role(self.INTERVIEWEE_STATUS)

    def is_admin(self):
        return self.is_role(self.ADMIN_ROLE)


class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    contact = models.ForeignKey(ContactDetails)
    updated = models.DateTimeField('company last update time', auto_now_add=True, blank=True)


class CompanyStaff(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    staff = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Job(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    updated = models.DateTimeField('question last update time', auto_now_add=True, blank=True)


class Question(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField('question last update time', auto_now_add=True, blank=True)


class JobQuestion(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class ApplicationQuestion(models.Model):
    interviewee_email = models.CharField(max_length=100)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    deadline = models.DateTimeField('Application deadline', null=True, blank=True)
    start_time = models.DateTimeField('Start answer time', null=True, blank=True)
    end_time = models.DateTimeField('End answer time', null=True, blank=True)


class Answer(models.Model):
    application_question = models.ForeignKey(ApplicationQuestion, on_delete=models.CASCADE)
    job_question = models.ForeignKey(JobQuestion, on_delete=models.CASCADE)
    answer = models.TextField(null=True, blank=True)





