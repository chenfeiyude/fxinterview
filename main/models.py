from django.db import models

# Create your models here.


class ContactDetails(models.Model):
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    address3 = models.CharField(max_length=100, blank=True)
    address4 = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)


class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    contact = models.ForeignKey(ContactDetails)
    updated = models.DateTimeField('company last update time', auto_now_add=True, blank=True)


class CompanyStaff(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # staff = models.ForeignKey(User, on_delete=models.CASCADE) # TODO enable this once user model is created


class Job(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    updated = models.DateTimeField('question last update time', auto_now_add=True, blank=True)


class Question(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField
    updated = models.DateTimeField('question last update time', auto_now_add=True, blank=True)


class JobQuestion(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class ApplicationQuestion(models.Model):
    interviewee_email = models.CharField(max_length=50)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    deadline = models.DateTimeField('Application deadline', null=True, blank=True)
    start_time = models.DateTimeField('Start answer time', null=True, blank=True)
    end_time = models.DateTimeField('End answer time', null=True, blank=True)


class Answer(models.Model):
    application_question = models.ForeignKey(ApplicationQuestion, on_delete=models.CASCADE)
    job_question = models.ForeignKey(JobQuestion, on_delete=models.CASCADE)
    answer = models.TextField(blank=True)





