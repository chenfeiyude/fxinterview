from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_protect

from .models import ApplicationQuestion, JobQuestion, Answer
import logging


def index(request):
    return check_user_role(request)


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
    job_questions = get_list_or_404(JobQuestion, job=application_question.job)

    # show the initial question at the first time
    return render(request, 'main/view_application_questions.html', {'application_question': application_question,
                                                                    'job_question': job_questions[0],
                                                                    'interviewee_email': interviewee_email})


def submit_answer(request):
    interviewee_email = request.POST.get('interviewee_email')
    application_question_id = request.POST.get('application_question_id')
    job_question_id = request.POST.get('job_question_id')
    answer_content = request.POST.get('answer_content')

    application_question = get_object_or_404(ApplicationQuestion, pk=application_question_id, interviewee_email=interviewee_email)
    job_question = get_object_or_404(JobQuestion, pk=job_question_id)

    answer, created = Answer.objects.update_or_create(application_question=application_question,
                                             job_question=job_question,
                                             defaults={"answer": answer_content})
    
    return render(request, 'main/view_application_questions.html', {'application_question': application_question,
                                                                    'job_question': job_question,
                                                                    'interviewee_email': interviewee_email,
                                                                    'answer':answer})
