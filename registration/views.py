from django.shortcuts import render
import logging
from django.contrib.auth import authenticate, login
from django.http import *
from .forms import FXCreateUserForm
from main.views import index

# Create your views here.


def register(request):
    if request.method == 'POST':
        user_form = FXCreateUserForm(request.POST)
        logging.info(user_form)
        logging.info(user_form.is_valid())

        if user_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password1']
            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            return HttpResponseRedirect('/accounts/home')
        else:
            return render(request, 'main/index.html', dict(form=user_form))

    return index(request)