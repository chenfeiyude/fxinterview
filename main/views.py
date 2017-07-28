from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import ApplicationQuestion, JobQuestion, Answer, Job, Question
import logging
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import CreateJobForm
from .utils.fx_string_utils import fx_format_date_b_d_y_h_m_s


def index(request):
    return render(request, 'main/index.html')


@login_required(login_url='/login/')
def check_user_role(request):
    user = request.user

    if user is None or user.is_anonymous:
        return render(request, 'main/index.html')
    elif user.profile.is_interviewee():
        return interviewee_home(request)
    elif user.profile.is_interviewer():
        return render(request, 'main/accounts/interviewer_home.html')
    elif user.profile.is_admin():
        return render(request, 'main/accounts/admin_home.html')


@login_required(login_url='/login/')
def view_jobs(request):
    user = request.user
    jobs = Job.objects.filter(company=user.profile.company)
    return render(request, 'main/accounts/jobs.html', {'jobs': jobs})


@login_required(login_url='/login/')
def create_job(request):
    if request.method == 'POST':
        create_job_form = CreateJobForm(request.POST)
        if create_job_form.is_valid():
            job = create_job_form.save(commit=False)
            job.company = request.user.profile.company
            job.save()
            questions_id = request.POST.getlist('question_id')
            for question_id in questions_id:
                job_question = JobQuestion(job=job, question=Question.objects.get(pk=question_id))
                job_question.save()
            return view_jobs(request)
        else:
            return render(request, 'main/accounts/create_job.html', {'form': create_job_form})
    else:
        questions = Question.objects.all()
        return render(request, 'main/accounts/create_job.html', {'questions': questions})


@login_required(login_url='/login/')
def delete_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    job.delete()
    return view_jobs(request)


@login_required(login_url='/login/')
def view_questions(request):
    return render(request, 'main/accounts/questions.html')


def view_application_questions(request, application_question_id):
    interviewee_email = request.GET.get('interviewee_email')
    logging.info(str(interviewee_email) + " is viewing application question with id " + str(application_question_id))
    application_question = get_object_or_404(ApplicationQuestion, pk=application_question_id, interviewee_email=interviewee_email)

    if application_question.start_time:
        job_questions = get_list_or_404(JobQuestion, job=application_question.job)
        job_question = job_questions[0]

        # show the initial question at the first time
        estimated_end_time = fx_format_date_b_d_y_h_m_s(application_question.get_estimated_end_time())
        return render(request, 'main/applications/view_application_questions.html',
                      {'application_question': application_question,
                       'job_question': job_question,
                       'interviewee_email': interviewee_email,
                       'estimated_end_time': estimated_end_time})
    else:
        # show welcome page
        return render(request, 'main/applications/welcome.html',
                      {'application_question': application_question,
                       'interviewee_email': interviewee_email})


def start_answer(request):
    interviewee_email = request.POST.get('interviewee_email')
    application_question_id = request.POST.get('application_question_id')
    application_question = get_object_or_404(ApplicationQuestion, pk=application_question_id, interviewee_email=interviewee_email)
    if not application_question.start_time:
        application_question.start_time = timezone.now()
        application_question.save()
    job_questions = get_list_or_404(JobQuestion, job=application_question.job)

    # show the initial question at the first time
    estimated_end_time = fx_format_date_b_d_y_h_m_s(application_question.get_estimated_end_time())
    return render(request, 'main/applications/view_application_questions.html', {'application_question': application_question,
                                                                    'job_question': job_questions[0],
                                                                    'interviewee_email': interviewee_email,
                                                                    'estimated_end_time': estimated_end_time})


def submit_answer(request):
    interviewee_email = request.POST.get('interviewee_email')
    application_question_id = request.POST.get('application_question_id')
    job_question_id = request.POST.get('job_question_id')
    answer_content = request.POST.get('answer_content')
    submit_action = request.POST.get('submit_action')
    prev_action = request.POST.get('prev_action')
    next_action = request.POST.get('next_action')

    application_question = get_object_or_404(ApplicationQuestion, pk=application_question_id, interviewee_email=interviewee_email)
    job_question = get_object_or_404(JobQuestion, pk=job_question_id)

    if submit_action is not None:
        answer, created = Answer.objects.update_or_create(application_question=application_question,
                                                          job_question=job_question,
                                                          defaults={"answer": answer_content})
    else:
        job_question_id = int(job_question_id)
        job_questions = get_list_or_404(JobQuestion, job=application_question.job)
        temp_last_id = None
        logging.info('current job q id : ' + str(job_question_id))
        for temp_question in job_questions:
            logging.info(temp_question.id)
            if prev_action is not None and job_question_id > temp_question.id:
                if temp_last_id is None or temp_question.id > temp_last_id:
                    temp_last_id = temp_question.id
                    job_question = temp_question
            elif next_action is not None and job_question_id < temp_question.id:
                if temp_last_id is None or temp_question.id < temp_last_id:
                    temp_last_id = temp_question.id
                    job_question = temp_question

        logging.info('final job q id : ' + str(job_question_id))
        answer, created = Answer.objects.get_or_create(application_question=application_question, job_question=job_question)
        if created:
            answer.answer = job_question.question.default_template
            answer.save()

    estimated_end_time = fx_format_date_b_d_y_h_m_s(application_question.get_estimated_end_time())
    return render(request, 'main/applications/view_application_questions.html', {'application_question': application_question,
                                                                                 'job_question': job_question,
                                                                                 'interviewee_email': interviewee_email,
                                                                                 'answer': answer,
                                                                                 'estimated_end_time': estimated_end_time})


@login_required(login_url='/login/')
def interviewee_home(request):
    user = request.user
    applications = ApplicationQuestion.objects.filter(interviewee_email=user.email)
    return render(request, 'main/accounts/interviewee_home.html', {'applications': applications})