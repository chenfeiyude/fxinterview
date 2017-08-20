from django import forms
from .models import Job, User, Profile, Question
from django.contrib.auth.forms import UserCreationForm


class JobForm(forms.ModelForm):
    name = forms.CharField(error_messages={'required': 'Job name is required'})
    description = forms.CharField(required=False, max_length=200,
                                  error_messages={'max_length': 'Ensure Description has at most 200 characters'})

    class Meta:
        model = Job
        fields = ('name', 'description', 'company')

    def clean(self):
        cleaned_data = super(JobForm, self).clean()
        name = cleaned_data.get('name')
        company = cleaned_data.get('company')

        if name and company and Job.objects.exclude(pk=self.instance.pk).filter(name=name, company=company).exists():
                raise forms.ValidationError({'name': ["Question name already exists", ]})

        return self.cleaned_data


class QuestionForm(forms.ModelForm):
    name = forms.CharField(error_messages={'required': 'Question name is required'})

    description = forms.CharField(required=False, max_length=200,
                                  error_messages={'max_length': 'Ensure Description has at most 200 characters'})

    default_template = forms.CharField(required=False)

    estimated_time_m = forms.IntegerField(required=False)

    class Meta:
        model = Question
        fields = ('name', 'description', 'company', 'default_template', 'estimated_time_m')

    def clean(self):
        cleaned_data = super(QuestionForm, self).clean()
        name = cleaned_data.get('name')
        company = cleaned_data.get('company')

        if name and company and Question.objects.exclude(pk=self.instance.pk).filter(name=name, company=company).exists():
            raise forms.ValidationError({'name': ["Question name already exists", ]})

        return self.cleaned_data


class FXCreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.IntegerField(required=True, widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'role', 'email')

    def save(self, commit=True):
        new_user = super(UserCreationForm, self).save(commit=False)
        password = self.cleaned_data['password1']
        email = self.cleaned_data['email']
        new_user.set_password(password)
        new_user.email = email

        new_profile = Profile(user=new_user, role=self.cleaned_data['role'])
        if commit:
            new_user.save()
            new_profile.user = new_user
            new_profile.save()

        return new_user
