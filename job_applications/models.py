import datetime

from django.db import models
from django.utils import timezone

from fx_tools.utils import fx_timezone_utils, fx_constants
from main.models import Job, JobQuestion


# Create your models here.


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
        app_label = "job_applications"
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
        app_label = "job_applications"
        unique_together = ('application_question', 'job_question',)