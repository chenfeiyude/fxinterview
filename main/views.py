from django.shortcuts import render, get_object_or_404

from .models import ApplicationQuestion

# Create your views here.


def index(request):
    return render(request, 'main/index.html')


def view_application_questions(request, application_question_id):
    application_question = None
    # application_question = get_object_or_404(ApplicationQuestion, pk=application_question_id)

    return render(request, 'interviewee/view_application_questions.html', {'application_question': application_question})