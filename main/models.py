from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from .utils import fx_timezone_utils, fx_constants

# Create your models here.


class ContactDetails(models.Model):
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    address3 = models.CharField(max_length=100, null=True, blank=True)
    address4 = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)


class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    contact = models.ForeignKey(ContactDetails)
    updated = models.DateTimeField('company last update time', auto_now_add=True, blank=True)


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
    contact_details = models.ForeignKey(ContactDetails, blank=True, null=True)
    validated = models.BooleanField(default=False)
    role = models.IntegerField(choices=ROLE_CHOICES, default=ADMIN_ROLE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)

    def __is_role(self, check_role):
        return self.role == check_role

    def is_interviewer(self):
        return self.__is_role(self.INTERVIEWER_STATUS)

    def is_interviewee(self):
        return self.__is_role(self.INTERVIEWEE_STATUS)

    def is_admin(self):
        return self.__is_role(self.ADMIN_ROLE)


class Job(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    updated = models.DateTimeField('question last update time', auto_now_add=True, blank=True)

    class Meta:
        unique_together = ('name', 'company',)

    def get_questions(self):
        job_question_list = JobQuestion.objects.filter(job=self)
        questions = []
        for job_question in job_question_list:
            questions.append(job_question.question)
        return questions


class Question(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    default_template = models.TextField(null=True, blank=True)
    estimated_time_m = models.IntegerField(default=0)
    updated = models.DateTimeField('question last update time', auto_now_add=True, blank=True)

    class Meta:
        unique_together = ('name', 'company',)


class JobQuestion(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class ApplicationQuestion(models.Model):
    INIT = 1
    PENDING = 2
    DONE = 3
    STATUS = (
        (INIT, 'Init'),
        (PENDING, 'Pending'),
        (DONE, 'Done'),
    )

    interviewee_email = models.CharField(max_length=100)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    deadline = models.DateTimeField('Application deadline', null=True, blank=True)
    start_time = models.DateTimeField('Start answer time', null=True, blank=True)
    end_time = models.DateTimeField('End answer time', null=True, blank=True)
    estimated_time_m = models.IntegerField(default=0)  # this estimated time is based on questions' total estimated time
    status = models.IntegerField(choices=STATUS, default=INIT)
    created = models.DateTimeField('Application created time', auto_now_add=True, blank=True)

    class Meta:
        ordering = ('-created',)

    def get_estimated_end_time(self):
        estimated_end_time = None
        if self.start_time and self.estimated_time_m:
            estimated_end_time = timezone.localtime(self.start_time + datetime.timedelta(minutes=self.estimated_time_m))
        return estimated_end_time

    def is_expired(self):
        estimated_end_time = self.get_estimated_end_time()
        if estimated_end_time and estimated_end_time < fx_timezone_utils.get_local_time_now():
            return True
        return False

    def is_init(self):
        return self.status == self.INIT

    def is_finished(self):
        return self.status == self.DONE

    def start(self):
        self.start_time = fx_timezone_utils.get_local_time_now()
        self.status = ApplicationQuestion.PENDING
        self.save()

    def finish(self):
        self.end_time = fx_timezone_utils.get_local_time_now()
        self.status = ApplicationQuestion.DONE
        self.save()


class Answer(models.Model):
    application_question = models.ForeignKey(ApplicationQuestion, on_delete=models.CASCADE)
    job_question = models.ForeignKey(JobQuestion, on_delete=models.CASCADE)
    answer = models.TextField(null=True, blank=True)
    selected_language = models.TextField(null=False, blank=False, default=fx_constants.LANGUAGE_PYTHON)

    class Meta:
        unique_together = ('application_question', 'job_question',)





