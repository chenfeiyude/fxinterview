from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /interviewer/
    url(r'^$', views.index, name='index'),
    # ex: /interviewer/company/1/
    url(r'^company/(?P<company_id>[0-9]+)/$', views.company_details, name='company_detail'),
]