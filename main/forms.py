from django import forms
from .models import Job, User, Profile


class CreateJobForm(forms.ModelForm):
    name = forms.CharField(error_messages={'required': 'Job name is required'})

    class Meta:
        model = Job
        fields = ('name', 'description',)


class ProfileForm(forms.ModelForm):
    role = forms.IntegerField(error_messages={'required': 'Role is required'})

    class Meta:
        model = Profile
        exclude = ['user']
        fields = ('role',)
