from django import forms
from .models import Job, User, Profile, Question, QuestionType
from django.contrib.auth.forms import UserCreationForm


class JobForm(forms.ModelForm):
    name = forms.CharField(max_length=100, error_messages={'required': 'Job name is required',
                                                           'max_length': 'Job name is too long.'})
    description = forms.CharField(required=False)

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
    name = forms.CharField(max_length=100, error_messages={'required': 'Question name is required',
                                                           'max_length': 'Question name is too long.'})

    description = forms.CharField(required=False)

    default_template = forms.CharField(required=False)

    estimated_time_m = forms.IntegerField(required=True, error_messages={'required': 'ETC is required, default set to 0'})

    question_type = forms.ModelChoiceField(queryset=QuestionType.objects.all())

    class Meta:
        model = Question
        fields = ('name', 'description', 'company', 'default_template', 'estimated_time_m', 'question_type')

    def clean(self):
        cleaned_data = super(QuestionForm, self).clean()
        name = cleaned_data.get('name')
        company = cleaned_data.get('company')

        if name and company and Question.objects.exclude(pk=self.instance.pk).filter(name=name, company=company).exists():
            raise forms.ValidationError({'name': ["Question name already exists", ]})

        return self.cleaned_data


class FXUpdateUserForm(forms.ModelForm):
    username = forms.CharField(required=True, widget=forms.HiddenInput())
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super(FXUpdateUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user


class ProfileForm(forms.Form):
    first_name = forms.CharField(error_messages={'required': 'First Name is required'})
    last_name = forms.CharField(error_messages={'required': 'Last Name is required'})
    email = forms.CharField(error_messages={'required': 'Email is required'})
    role = forms.CharField(error_messages={'required': 'Role is required'})
    is_active = forms.CharField(error_messages={'required': 'Active is required'})


