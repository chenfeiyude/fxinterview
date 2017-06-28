from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^interviewee/application/(?P<application_question_id>[0-9]+)$', views.view_application_questions, name='view_application_questions'),
]