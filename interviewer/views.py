from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Company

# Create your views here.


def index(request):
    try:
        #TODO do something here
        context = {
            'message': "hellow world",
        }
        return render(request, 'interviewer/index.html', context)
    except:
        raise Http404("XX does not exist")

def company_details(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    return render(request, 'interviewer/company_detail.html', {'company': company})
