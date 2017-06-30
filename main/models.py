from django.db import models
from django.contrib.auth.models import User

class ContactDetails(models.Model):
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    address3 = models.CharField(max_length=100)
    address4 = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contactDetails = models.ForeignKey(ContactDetails, on_delete=models.CASCADE)
    validated = models.BooleanField(default=False)
    role = models.CharField(max_length=100)


class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField
    contact = models.ForeignKey(ContactDetails)
    updated = models.DateTimeField('company last update time')


class CompanyStaff(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # staff = models.ForeignKey(User, on_delete=models.CASCADE) # TODO enable this once user model is created


class Job(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    updated = models.DateTimeField('question last update time')


class Question(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField
    updated = models.DateTimeField('question last update time')


class JobQuestion(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class ApplicationQuestion(models.Model):
    # interviewee = models.ForeignKey(User, on_delete=models.CASCADE) # TODO enable this once user model is created
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    deadline = models.DateTimeField('Application deadline')
    start_time = models.DateTimeField('Start answer time')
    end_time = models.DateTimeField('End answer time')


class Answer(models.Model):
    application_question = models.ForeignKey(ApplicationQuestion, on_delete=models.CASCADE)
    job_question = models.ForeignKey(JobQuestion, on_delete=models.CASCADE)
    answer = models.TextField





