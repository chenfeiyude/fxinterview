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


class QuestionForm(forms.ModelForm):
    name = forms.CharField(error_messages={'required': 'Question name is required'})

    description = forms.CharField(required=False, max_length=200,
                                  error_messages={'max_length': 'Ensure Description has at most 200 characters'})

    default_template = forms.CharField(required=False)

    estimated_time_m = forms.IntegerField(required=False)

    class Meta:
        model = Question
        fields = ('name', 'description', 'company', 'default_template', 'estimated_time_m')


class FXCreateUserForm(UserCreationForm):
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
