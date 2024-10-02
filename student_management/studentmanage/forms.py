import re
from django import forms
from .models import Student
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]  

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'enrollment_date', 'grade']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            raise forms.ValidationError('please enter a valid email address')
        return email

    def clean_grade(self):
        grade = self.cleaned_data.get('grade')
        if grade < 1 or grade > 12:
            raise forms.ValidationError('grade must be between 1 and 12')
        return grade
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise ValidationError('The two password fields didn’t match')
        return cd.get('password2')