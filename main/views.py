from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from .models import ApplicationQuestion, JobQuestion, Answer, Job, Question, Profile
import logging
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from .forms import JobForm, FXCreateUserForm, QuestionForm
from .utils import fx_string_utils


def index(request):
    user_form = FXCreateUserForm(initial={'role': Profile.INTERVIEWEE_STATUS })
    # profile_form = ProfileForm(initial={'role': Profile.INTERVIEWEE_STATUS })

    return render(request, 'main/index.html', dict(form=user_form))


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
    questions = Question.objects.all()
    if request.method == 'POST':
        create_job_form = JobForm(request.POST)
        if create_job_form.is_valid():
            job = create_job_form.save(commit=False)
            job.save()
            question_ids = request.POST.getlist('question_id')
            for question_id in question_ids:
                job_question = JobQuestion(job=job, question=Question.objects.get(pk=question_id))
                job_question.save()
            return HttpResponseRedirect(reverse('main:view_jobs'))
        else:
            return render(request, 'main/accounts/create_job.html', {'form': create_job_form, 'questions': questions})
    else:
        return render(request, 'main/accounts/create_job.html', {'questions': questions})


@login_required(login_url='/login/')
def create_question(request):
    if request.method == 'POST':
        create_question_form = QuestionForm(request.POST)
        if create_question_form.is_valid():
            question = create_question_form.save(commit=False)
            question.save()
            return HttpResponseRedirect(reverse('main:view_questions'))
        else:
            return render(request, 'main/accounts/create_question.html', {'form': create_question_form})
    else:
        return render(request, 'main/accounts/create_question.html')


@login_required(login_url='/login/')
def edit_job(request):
    if request.method == 'POST':
        job = get_object_or_404(Job, pk=request.POST.get('id'))
        update_job_form = JobForm(request.POST, instance=job)
        if update_job_form.is_valid():
            job = update_job_form.save()
            question_ids = request.POST.getlist('question_id')
            JobQuestion.objects.filter(job=job).delete()
            for question_id in question_ids:
                job_question = JobQuestion(job=job, question=Question.objects.get(pk=question_id))
                job_question.save()
            return HttpResponseRedirect(reverse('main:view_jobs'))
        else:
            return __configure_edit_job(request, job=job, job_form=update_job_form)
    else:
        job = get_object_or_404(Job, pk=request.GET.get('id'))
        return __configure_edit_job(request, job=job)


def __configure_edit_job(request, job, job_form=None):
    job_questions = JobQuestion.objects.filter(job=job)
    assigned_questions = []
    temp_id = []
    for job_question in job_questions:
        question = get_object_or_404(Question, pk=job_question.question.id)
        assigned_questions.append(question)
        temp_id.append(question.id)
    questions = Question.objects.all().exclude(id__in=temp_id)
    return render(request, 'main/accounts/edit_job.html',
                  {'form': job_form, 'job': job, 'questions': questions, 'assigned_questions': assigned_questions})


@login_required(login_url='/login/')
def delete_job(request):
    job = get_object_or_404(Job, pk=request.GET.get('id'))
    job.delete()
    return HttpResponseRedirect(reverse('main:view_jobs'))


@login_required(login_url='/login/')
def delete_question(request):
    question = get_object_or_404(Question, pk=request.GET.get('id'))
    question.delete()
    return HttpResponseRedirect(reverse('main:view_questions'))


@login_required(login_url='/login/')
def view_questions(request):
    user = request.user
    questions = Question.objects.filter(company=user.profile.company)
    return render(request, 'main/accounts/questions.html', {'questions': questions})


def view_application_questions(request, application_question_id):
    interviewee_email = request.GET.get('interviewee_email')
    if interviewee_email is None:
        interviewee_email = request.POST.get('interviewee_email')
    logging.info(str(interviewee_email) + " is viewing application question with id " + str(application_question_id))
    application_question = get_object_or_404(ApplicationQuestion, pk=application_question_id, interviewee_email=interviewee_email)

    if application_question.start_time:
        job_questions = get_list_or_404(JobQuestion, job=application_question.job)
        job_question = job_questions[0]
        answer = Answer.objects.filter(application_question=application_question, job_question=job_question).first()
        # show the initial question at the first time
        estimated_end_time = fx_string_utils.format_date_b_d_y_h_m_s(application_question.get_estimated_end_time())
        return render(request, 'main/applications/view_application_questions.html',
                      {'application_question': application_question,
                       'job_question': job_question,
                       'interviewee_email': interviewee_email,
                       'estimated_end_time': estimated_end_time,
                       'answer': answer})
    else:
        # show welcome page
        return render(request, 'main/applications/welcome.html',
                      {'application_question': application_question,
                       'interviewee_email': interviewee_email})


def start_answer(request):
    interviewee_email = request.POST.get('interviewee_email')
    application_question_id = request.POST.get('application_question_id')
    application_question = get_object_or_404(ApplicationQuestion, pk=application_question_id, interviewee_email=interviewee_email)
    if application_question.is_init():
        application_question.start()

    job_questions = get_list_or_404(JobQuestion, job=application_question.job)

    # show the initial question at the first time
    estimated_end_time = fx_string_utils.format_date_b_d_y_h_m_s(application_question.get_estimated_end_time())
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

    if submit_action is not None and not application_question.is_expired():
        answer, created = Answer.objects.update_or_create(application_question=application_question,
                                                          job_question=job_question,
                                                          defaults={"answer": answer_content})
    else:
        job_question_id = int(job_question_id)
        job_questions = get_list_or_404(JobQuestion, job=application_question.job)
        temp_last_id = None
        logging.info('current job q id : ' + str(job_question_id))
        for temp_question in job_questions:
            if prev_action is not None and job_question_id > temp_question.id:
                if temp_last_id is None or temp_question.id > temp_last_id:
                    temp_last_id = temp_question.id
                    job_question = temp_question
            elif next_action is not None and job_question_id < temp_question.id:
                if temp_last_id is None or temp_question.id < temp_last_id:
                    temp_last_id = temp_question.id
                    job_question = temp_question

        logging.info('final job q id : ' + str(job_question_id))
        answer = Answer.objects.filter(application_question=application_question, job_question=job_question).first()

    estimated_end_time = fx_string_utils.format_date_b_d_y_h_m_s(application_question.get_estimated_end_time())
    return render(request, 'main/applications/view_application_questions.html', {'application_question': application_question,
                                                                                 'job_question': job_question,
                                                                                 'interviewee_email': interviewee_email,
                                                                                 'answer': answer,
                                                                                 'estimated_end_time': estimated_end_time,
                                                                                 'is_expired': application_question.is_expired()})


def finish_answer(request):
    interviewee_email = request.POST.get('interviewee_email')
    application_question_id = request.POST.get('application_question_id')

    application_question = get_object_or_404(ApplicationQuestion, pk=application_question_id, interviewee_email=interviewee_email)

    if not application_question.is_finished():
        application_question.finish()

    return view_application_questions(request, application_question_id)


@login_required(login_url='/login/')
def interviewee_home(request):
    user = request.user
    applications = ApplicationQuestion.objects.filter(interviewee_email=user.email)
    return render(request, 'main/accounts/interviewee_home.html', {'applications': applications})


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