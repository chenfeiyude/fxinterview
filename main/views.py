from django.shortcuts import render, get_object_or_404

from .models import ApplicationQuestion
from .models import Profile
import logging


def index(request):
    return render(request, 'main/index.html')


def check_user_role(request):
    profile_role = Profile.objects.get(user_id=request.user.id).role
    # user role has default value so it cannot null
    if(Profile.INTERVIEWEE_STATUS == profile_role):
        return render(request, 'main/interviewee_home.html')
    else:
        return render(request, 'main/interviewer_home.html')


def view_application_questions(request, application_question_id):
    interviewee_email = request.GET.get('interviewee_email')
    logging.info(interviewee_email)
    application_question = get_object_or_404(ApplicationQuestion, pk=application_question_id, interviewee_email=interviewee_email)
    return render(request, 'main/view_application_questions.html', {'application_question': application_question})