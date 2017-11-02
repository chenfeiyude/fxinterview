from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import ApplicationQuestion, JobQuestion, Answer
import logging
from main.utils import fx_string_utils, fx_constants
from .code_executor.fx_executor_factory import FXExecutorFactory

# Create your views here.


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
        return render(request, 'job_applications/view_application_questions.html',
                      {'application_question': application_question,
                       'job_question': job_question,
                       'interviewee_email': interviewee_email,
                       'estimated_end_time': estimated_end_time,
                       'answer': answer,
                       'support_languages': fx_constants.SUPPORT_LANGUAGES})
    else:
        # show welcome page
        return render(request, 'job_applications/welcome.html',
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
    return render(request, 'job_applications/view_application_questions.html', {'application_question': application_question,
                                                                    'job_question': job_questions[0],
                                                                    'interviewee_email': interviewee_email,
                                                                    'estimated_end_time': estimated_end_time,
                                                                    'support_languages': fx_constants.SUPPORT_LANGUAGES})


def submit_answer(request):
    interviewee_email = request.POST.get('interviewee_email')
    application_question_id = request.POST.get('application_question_id')
    job_question_id = request.POST.get('job_question_id')
    answer_content = request.POST.get('answer_content')
    selected_language = request.POST.get('selected_language')
    submit_action = request.POST.get('submit_action')
    prev_action = request.POST.get('prev_action')
    next_action = request.POST.get('next_action')
    run_action = request.POST.get('run_action')

    application_question = get_object_or_404(ApplicationQuestion, pk=application_question_id, interviewee_email=interviewee_email)
    job_question = get_object_or_404(JobQuestion, pk=job_question_id)

    run_results = None
    if submit_action is not None or run_action is not None:
        if not application_question.is_expired():
            answer, created = Answer.objects.update_or_create(application_question=application_question,
                                                              job_question=job_question,
                                                              defaults={"answer": answer_content,
                                                                        "selected_language": selected_language})
        else:
            answer = Answer.objects.filter(application_question=application_question, job_question=job_question).first()

        if run_action is not None:
            executor = FXExecutorFactory.get_executor(selected_language)
            if executor:
                run_results = executor.run_code(answer_content)
            else:
                run_results = {fx_constants.KEY_CODE: fx_constants.KEY_CODE_ERROR,
                               fx_constants.KEY_OUTPUT: 'Language not supported'}
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
    return render(request, 'job_applications/view_application_questions.html', {'application_question': application_question,
                                                                                 'job_question': job_question,
                                                                                 'interviewee_email': interviewee_email,
                                                                                 'answer': answer,
                                                                                 'run_results': run_results,
                                                                                 'estimated_end_time': estimated_end_time,
                                                                                 'support_languages': fx_constants.SUPPORT_LANGUAGES,
                                                                                 'is_expired': application_question.is_expired()})


def finish_answer(request):
    interviewee_email = request.POST.get('interviewee_email')
    application_question_id = request.POST.get('application_question_id')

    application_question = get_object_or_404(ApplicationQuestion, pk=application_question_id, interviewee_email=interviewee_email)

    if not application_question.is_finished():
        application_question.finish()

    return view_application_questions(request, application_question_id)