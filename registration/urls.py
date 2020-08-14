from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

# name space for url
# e.g you can call {% url 'main.view_application_questions' xxx.id %} instead of hard code url in html

# app_name = 'registration'

urlpatterns = [
    # http://localhost:8000/register/
    url(r'^register/$', views.register, name='register'),
    # http://localhost:8000/accounts/login/
    url(r'^accounts/login/$', auth_views.LoginView, {'template_name': 'registration/login.html'}, name='login'),
    # http://localhost:8000/accounts/logout/
    url(r'^accounts/logout/$', auth_views.LogoutView, {'next_page': '/'}, name='logout'),
    # http://localhost:8000/password_change/
    # url(r'^password_change/$', auth_views.PasswordChangeView.as_view(success_url='/password_change/done'), name='password_change'),
    url(r'^password_change/$', auth_views.PasswordChangeView, {'template_name': 'registration/password_change.html'},
        name='password_change'),
    # http://localhost:8000/password_change/done
    # url(r'^password_change/done/$', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    url(r'^password_change/done/$', auth_views.PasswordChangeDoneView,
        {'template_name': 'registration/password_change_done.html'}, name='password_change_done'),
    # http://localhost:8000/password_reset/
    # url(r'^password_reset/$', auth_views.PasswordResetView.as_view(success_url='/password_reset/done', from_email='support@fxinterview.com'), name='password_reset'),
    url(r'^password_reset/$', auth_views.PasswordResetView, {'template_name': 'registration/password_reset.html'},
        name='password_reset'),
    # http://localhost:8000/password_reset/done
    # url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView,
        {'template_name': 'registration/password_reset_done.html'}, name='password_reset_done'),
    # http://localhost:8000/password_reset/confirm
    # url(r'^password_reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     auth_views.PasswordResetConfirmView.as_view(success_url='/password_reset/complete'), name='password_reset_confirm'),
    url(r'^password_reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView, {'template_name': 'registration/password_reset_confirm.html'},
        name='password_reset_confirm'),
    # http://localhost:8000/password_reset/complete
    # url(r'^password_reset/complete/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    url(r'^password_reset/complete/$', auth_views.PasswordResetCompleteView,
        {'template_name': 'registration/password_reset_complete.html'}, name='password_reset_complete'),
]
