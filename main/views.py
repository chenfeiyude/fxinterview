from django.shortcuts import render, get_object_or_404

from .models import ApplicationQuestion
import logging
# from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'main/index.html')


# @login_required(login_url='/login/')
def check_user_role(request):
    user = request.user

    if user is None or user.is_anonymous:
        return render(request, 'main/index.html')
    elif user.profile.is_interviewee():
        return render(request, 'main/interviewee_home.html')
    elif user.profile.is_interviewer():
        return render(request, 'main/interviewer_home.html')
    elif user.profile.is_admin():
        return render(request, 'main/admin_home.html')


def view_application_questions(request, application_question_id):
    interviewee_email = request.GET.get('interviewee_email')
    logging.info(str(interviewee_email) + " is viewing application question with id " + str(application_question_id))
    application_question = get_object_or_404(ApplicationQuestion, pk=application_question_id, interviewee_email=interviewee_email)
    return render(request, 'main/view_application_questions.html', {'application_question': application_question})
