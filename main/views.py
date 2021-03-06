import logging

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import *
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from fx_tools.code_executor.fx_executor_factory import FXExecutorFactory
from fx_tools.utils import email_utils, fx_request_parameters, fx_string_utils
from fx_tools.utils import fx_constants
from job_applications.models import ApplicationQuestion
from registration.forms import FXCreateUserForm
from .forms import JobForm, QuestionForm, FXUpdateUserForm, ProfileForm
from .models import JobQuestion, Job, Question, Profile, User, QuestionType


def index(request):
    user_form = FXCreateUserForm(initial={'role': Profile.INTERVIEWEE_ROLE })
    # profile_form = ProfileForm(initial={'role': Profile.INTERVIEWEE_ROLE })

    return render(request, 'main/index.html', {'form': user_form, 'support_languages': fx_constants.SUPPORT_LANGUAGES})


@login_required(login_url='/login/')
def check_user_role(request):
    user = request.user
    if user is None or user.is_anonymous:
        return render(request, 'main/index.html')
    elif user.profile.is_interviewee():
        return interviewee_home(request)
    elif user.profile.is_interviewer():
        return __render_interviewer_admin_page(request, 'main/accounts/interviewer_home.html')
    elif user.profile.is_admin():
        return __render_interviewer_admin_page(request, 'main/accounts/admin_home.html')


@login_required(login_url='/login/')
def interviewee_home(request):
    user = request.user
    applications = ApplicationQuestion.objects.filter(interviewee_email=user.email)
    page = request.GET.get(fx_request_parameters.page)
    applications = __get_pagination_list(applications, page)
    return render(request, 'main/accounts/interviewee_home.html', {'applications': applications,
                                                                   'user': user,
                                                                   'page_range': applications.paginator.page_range})


def __render_interviewer_admin_page(request, url):
    user = request.user
    page = request.GET.get(fx_request_parameters.page)
    applications = []
    jobs = Job.objects.filter(company=user.profile.company)
    for job in jobs:
        applications.extend(ApplicationQuestion.objects.filter(job_id=job.id))

    applications = __get_pagination_list(applications, page)
    return render(request, url, {'applications': applications,
                                 'user': user,
                                 'page_range': applications.paginator.page_range})


def __get_pagination_list(original_list, page):
    paginator = Paginator(original_list, fx_constants.DEFAULT_PER_PAGE)
    try:
        pagination_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        pagination_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        pagination_list = paginator.page(paginator.num_pages)
    return pagination_list


@login_required(login_url='/login/')
def view_jobs(request):
    user = request.user
    jobs = Job.objects.filter(company=user.profile.company)
    page = request.GET.get(fx_request_parameters.page)
    jobs = __get_pagination_list(jobs, page)
    return render(request, 'main/accounts/view_jobs.html', {'jobs': jobs,
                                 'page_range': jobs.paginator.page_range})


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
    question_types = QuestionType.objects.all()
    if request.method == 'POST':
        create_question_form = QuestionForm(request.POST)
        if create_question_form.is_valid():
            question = create_question_form.save(commit=False)
            question.save()
            return HttpResponseRedirect(reverse('main:view_questions'))
        else:
            return render(request, 'main/accounts/create_question.html', {'form': create_question_form, 'question_types': question_types})
    else:
        return render(request, 'main/accounts/create_question.html', {'question_types': question_types})


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


@login_required(login_url='/login/')
def edit_question(request):
    if request.method == 'POST':
        question = get_object_or_404(Question, pk=request.POST.get('id'))
        update_question_form = QuestionForm(request.POST, instance=question)
        if update_question_form.is_valid():
            update_question_form.save()
            return HttpResponseRedirect(reverse('main:view_questions'))
        else:
            return __configure_edit_question(request, question=question, question_form=update_question_form)
    else:
        question = get_object_or_404(Question, pk=request.GET.get('id'))
        return __configure_edit_question(request, question=question)


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


def __configure_edit_question(request, question, question_form=None):
    question_types = QuestionType.objects.all()
    return render(request, 'main/accounts/edit_question.html',
                  {'form': question_form, 'question': question, 'question_types': question_types})


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
    page = request.GET.get(fx_request_parameters.page)
    questions = __get_pagination_list(questions, page)
    return render(request, 'main/accounts/view_questions.html', {'questions': questions,
                                                            'page_range': questions.paginator.page_range})


@login_required(login_url='/login/')
def view_profile(request):
    user = request.user
    form = FXUpdateUserForm()
    return __configure_profile(request, user, form)


@login_required(login_url='/login/')
def view_manage_interviewers(request):
    user = request.user
    interviewers = []
    if user.profile.is_admin():
        company = request.user.profile.company
        profiles = Profile.objects.filter(company=company)
        for profile in profiles:
            if user.username != profile.user.username:
                interviewers.append(profile.user)
    return render(request, 'main/accounts/view_manage_interviewers.html',
                  {'user': user, 'interviewers': interviewers})


@login_required(login_url='/login/')
def update_profile(request):
    user = request.user
    form = FXUpdateUserForm(request.POST, instance=request.user)
    if form.is_valid():
        form.save()
    else:
        logging.info(form.errors)

    return __configure_profile(request, user, form)


@login_required(login_url='/login/')
def edit_interviewer(request):

    if request.method == 'POST':
        interviewer = get_object_or_404(User, pk=request.POST.get('id'))
        form = ProfileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            interviewer.first_name = data['first_name']
            interviewer.last_name = data['last_name']
            interviewer.email = data['email']
            interviewer.profile.role = data['role']

            if data['is_active'] == 'True':
                interviewer.is_active = True
            else:
                interviewer.is_active = False

            interviewer.save()
            interviewer.profile.save()

        return render(request, 'main/accounts/edit_interviewer.html', {'interviewer': interviewer,
                                                                       'form': form,
                                                                       'success_message': interviewer.username + ' has been updated successfully',
                                                                       })
    else:
        interviewer = get_object_or_404(User, pk=request.GET.get('id'))
        return render(request, 'main/accounts/edit_interviewer.html', {'interviewer': interviewer})


def __configure_profile(request, user, form):
    return render(request, 'main/accounts/view_profile.html',
                  {'user': user, 'form': form})


@login_required(login_url='/login/')
def send_job_invitation(request):
    interviewee_email = request.POST.get('interviewee_email')
    email_job_id = request.POST.get('email_job_id')

    expire_date = None
    if request.POST.get('expire_date'):
        expire_date = request.POST.get('expire_date')
    job = get_object_or_404(Job, pk=email_job_id)

    job_questions = JobQuestion.objects.filter(job=job)

    estimated_time = 0
    for job_question in job_questions:
        question = get_object_or_404(Question, pk=job_question.question.id)
        estimated_time += question.estimated_time_m

    application_question = ApplicationQuestion.objects.create(interviewee_email=interviewee_email,
                                                              estimated_time_m=estimated_time,
                                                              end_time=expire_date,
                                                              job=job)
    application_question.save()

    full_url = fx_string_utils.get_domain_url(request) + '/application/' + str(application_question.id) + '?interviewee_email=' + interviewee_email

    email_utils.send_email("Job Invitation ("+job.name+")",
                           "Congratulation, you got an job invitation, please visit "+full_url,
                           interviewee_email)

    jobs = Job.objects.filter(company=request.user.profile.company)
    return render(request, 'main/accounts/jobs.html', {'jobs': jobs,
                                                       'success_message': 'An invitation email has been sent to '
                                                                          + interviewee_email})


def test_code(request):
    user_form = FXCreateUserForm(initial={'role': Profile.INTERVIEWEE_ROLE})
    answer_content = request.POST.get('answer_content')
    selected_language = request.POST.get('selected_language')

    executor = FXExecutorFactory.get_executor(selected_language)
    if executor:
        run_results = executor.run_code(answer_content)
    else:
        run_results = {fx_constants.KEY_CODE: fx_constants.KEY_CODE_ERROR,
                       fx_constants.KEY_OUTPUT: 'Language not supported'}

    return render(request, 'main/index.html',
                  {'run_results': run_results,
                   'selected_language': selected_language,
                   'support_languages': fx_constants.SUPPORT_LANGUAGES,
                   'form': user_form
                   })


def error_400(request, exception):
    logging.error(exception)
    return render(request, 'main/errors/400.html', status=400)


def error_401(request, exception):
    logging.error(exception)
    return render(request, 'main/errors/401.html', status=401)


def error_403(request, exception):
    logging.error(exception)
    return render(request, 'main/errors/403.html', status=403)


def error_404(request, exception):
    logging.error(exception)
    return render(request, 'main/errors/404.html', status=404)


def error_500(request):
    logging.error(request)
    return render(request, 'main/errors/500.html', status=500)