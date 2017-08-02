from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import ApplicationQuestion, JobQuestion, Answer, Job, Question, Profile
import logging
from django.utils import timezone
from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponseRedirect

from .forms import CreateJobForm, ProfileForm
from .utils import fx_string_utils
from .utils import fx_timezone_utils


def index(request):
    user_form = UserCreationForm()
    profile_form = ProfileForm()

    return render(request, 'main/index.html', dict(user_form=user_form,
                                                   profile_form=profile_form,
                                                   role=Profile.INTERVIEWEE_STATUS))


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
        estimated_end_time = fx_string_utils.format_date_b_d_y_h_m_s(application_question.get_estimated_end_time())
        return render(request, 'main/applications/view_application_questions.html',
                      {'application_question': application_question,
                       'job_question': job_question,
                       'interviewee_email': interviewee_email,
                       'estimated_end_time': estimated_end_time,
                       'is_expired': application_question.is_expired()})
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
        application_question.start_time = fx_timezone_utils.get_local_time_now();
        logging.info(application_question.start_time)
        application_question.save()
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


@login_required(login_url='/login/')
def interviewee_home(request):
    user = request.user
    applications = ApplicationQuestion.objects.filter(interviewee_email=user.email)
    return render(request, 'main/accounts/interviewee_home.html', {'applications': applications})


def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST, prefix='user')
        profile_form = ProfileForm(request.POST, prefix='profile')

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password1']

            user.set_password(password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            return HttpResponseRedirect('/accounts/home')
        else:
            return render(request, 'main/index.html', dict(user_form=user_form,
                                                           profile_form=profile_form,
                                                           role=Profile.INTERVIEWEE_STATUS))
    return index(request)