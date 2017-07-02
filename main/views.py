from django.shortcuts import render, get_object_or_404

from .models import ApplicationQuestion
import logging

# Create your views here.


def index(request):
    return render(request, 'main/index.html')


def view_application_questions(request, application_question_id):
    interviewee_email = request.GET.get('interviewee_email')
    logging.info(interviewee_email)
    application_question = get_object_or_404(ApplicationQuestion, pk=application_question_id, interviewee_email=interviewee_email)
    return render(request, 'main/view_application_questions.html', {'application_question': application_question})