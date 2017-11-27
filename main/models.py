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

    class Meta:
        app_label = "main"


class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    contact = models.ForeignKey(ContactDetails)
    updated = models.DateTimeField('company last update time', auto_now_add=True, blank=True)

    class Meta:
        app_label = "main"


class Profile(models.Model):
    ADMIN_ROLE = 1
    INTERVIEWER_ROLE = 2
    INTERVIEWEE_ROLE = 3
    ROLE_CHOICES = (
        (ADMIN_ROLE, 'Admin'),
        (INTERVIEWER_ROLE, 'interviewer'),
        (INTERVIEWEE_ROLE, 'interviewee'),
    )

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    contact_details = models.ForeignKey(ContactDetails, blank=True, null=True)
    validated = models.BooleanField(default=False)
    role = models.IntegerField(choices=ROLE_CHOICES, default=ADMIN_ROLE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        app_label = "main"

    def __is_role(self, check_role):
        return self.role == check_role

    def is_interviewer(self):
        return self.__is_role(self.INTERVIEWER_ROLE)

    def is_interviewee(self):
        return self.__is_role(self.INTERVIEWEE_ROLE)

    def is_admin(self):
        return self.__is_role(self.ADMIN_ROLE)


class Job(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    updated = models.DateTimeField('question last update time', auto_now_add=True, blank=True)

    class Meta:
        app_label = "main"
        unique_together = ('name', 'company',)

    def get_questions(self):
        job_question_list = JobQuestion.objects.filter(job=self)
        questions = []
        for job_question in job_question_list:
            questions.append(job_question.question)
        return questions


class QuestionType(models.Model):
    GENERAL_TYPE = 1
    CODING_TYPE = 2
    QUESTION_TYPE_CHOICES = (
        (GENERAL_TYPE, 'General'),
        (CODING_TYPE, 'Coding'),
    )

    type = models.IntegerField(choices=QUESTION_TYPE_CHOICES, default=GENERAL_TYPE)
    display_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    class Meta:
        app_label = "main"

    def __is_question_type(self, check_question_type):
        return self.type == check_question_type

    def is_general_type(self):
        return self.__is_question_type(self.GENERAL_TYPE)

    def is_coding_type(self):
        return self.__is_question_type(self.CODING_TYPE)


class Question(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    default_template = models.TextField(null=True, blank=True)
    estimated_time_m = models.IntegerField(default=0)
    updated = models.DateTimeField('question last update time', auto_now_add=True, blank=True)
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)

    class Meta:
        app_label = "main"
        unique_together = ('name', 'company',)


class JobQuestion(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        app_label = "main"







