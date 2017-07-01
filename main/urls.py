from django.conf.urls import url

from . import views
from django.contrib.auth import views as auth_views

# name space for url
# e.g you can call {% url 'main.view_application_questions' xxx.id %} instead of hard code url in html

app_name = 'main'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # http://localhost:8000/login/
    url(r'^login/$', auth_views.login, {'template_name': 'main/login.html'}),
    # http://localhost:8000/application/1?interviewee_email=xuxiang1990619@gmail.com
    url(r'^application/(?P<application_question_id>[0-9]+)$', views.view_application_questions, name='view_application_questions'),
]