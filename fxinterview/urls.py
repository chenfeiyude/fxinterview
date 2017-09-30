"""fxinterview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    # http://localhost:8000/admin/
    url(r'^admin/', admin.site.urls),
    url(r'^', include('main.urls')),
    # http://localhost:8000/accounts/login/
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'main/login.html'}, name='login'),
    # http://localhost:8000/accounts/logout/
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    # http://localhost:8000/password_change/
    url(r'^password_change/$', auth_views.PasswordChangeView.as_view(success_url='/password_change/done'), name='password_change'),
    # http://localhost:8000/password_change/done
    url(r'^password_change/done/$', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # http://localhost:8000/password_reset/
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(success_url='/password_reset/done', from_email='support@fxinterview.com'), name='password_reset'),
    # http://localhost:8000/password_reset/done
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # http://localhost:8000/password_reset/confirm
    url(r'^password_reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(success_url='/password_reset/complete'), name='password_reset_confirm'),
    # http://localhost:8000/password_reset/complete
    url(r'^password_reset/complete/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
