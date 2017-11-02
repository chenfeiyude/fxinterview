from django.conf.urls import url, include

from . import views
from django.contrib.auth import views as auth_views

# name space for url
# e.g you can call {% url 'main.view_application_questions' xxx.id %} instead of hard code url in html

app_name = 'job_applications'

urlpatterns = [
    # http://localhost:8000/application/2?interviewee_email=interviewee@fxinterview.com
    url(r'^application/(?P<application_question_id>[0-9]+)$', views.view_application_questions, name='view_application_questions'),
    # http://localhost:8000/application/start_answer$
    url(r'^application/start_answer', views.start_answer, name='start_answer'),
    # http://localhost:8000/application/submit_answer
    url(r'^application/submit_answer', views.submit_answer, name='submit_answer'),
    # http://localhost:8000/application/finish_answer
    url(r'^application/finish_answer', views.finish_answer, name='finish_answer'),
]

