from django import forms
from .models import Job


class CreateJobForm(forms.ModelForm):
    name = forms.CharField(error_messages={'required': 'Job name is required'})

    class Meta:
        model = Job
        fields = ('name', 'description',)

