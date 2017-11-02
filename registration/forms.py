from django import forms
from main.models import User, Profile
from django.contrib.auth.forms import UserCreationForm


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