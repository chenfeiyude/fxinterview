from django.conf.urls import url

from . import views
from django.contrib.auth import views as auth_views

# name space for url
# e.g you can call {% url 'main.view_application_questions' xxx.id %} instead of hard code url in html

app_name = 'main'
urlpatterns = [
    # http://localhost:8000/
    url(r'^$', views.index, name='index'),
    # http://localhost:8000/login/
    url(r'^login/$', auth_views.login, {'template_name': 'main/login.html'}, name='login'),
    # http://localhost:8000/logout/
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    # http://localhost:8000/accounts/home
    url(r'^accounts/home/$', views.check_user_role, name='view_home'),
    # http://localhost:8000/accounts/jobs
    url(r'^accounts/jobs/$', views.view_jobs, name='view_jobs'),
    # http://localhost:8000/accounts/create_job
    url(r'^accounts/create_job/$', views.create_job, name='create_job'),
    # http://localhost:8000/accounts/questions
    url(r'^accounts/questions/$', views.view_questions, name='view_questions'),
    # http://localhost:8000/application/2?interviewee_email=interviewee@fxinterview.com
    url(r'^application/(?P<application_question_id>[0-9]+)$', views.view_application_questions, name='view_application_questions'),
    # http://localhost:8000/application/submit_answer
    url(r'^application/submit_answer', views.submit_answer, name='submit_answer'),

]