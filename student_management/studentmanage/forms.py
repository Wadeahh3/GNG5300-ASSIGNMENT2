import re
from django import forms
from .models import Student
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date

# RegisterForm for user registration, extends UserCreationForm
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Email is required

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():  # Check if email is unique
            raise ValidationError("This email address is already registered.")
        return email

# StudentForm for student creation and update
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'enrollment_date', 'grade']

    # Email validation to ensure correct format
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            raise forms.ValidationError('Please enter a valid email address')
        return email

    # Grade validation to ensure it's between 1 and 12
    def clean_grade(self):
        grade = self.cleaned_data.get('grade')
        if grade < 1 or grade > 12:
            raise forms.ValidationError('Grade must be between 1 and 12')
        return grade

    # Date of birth validation to ensure it's a valid date and in the past
    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob > date.today():
            raise ValidationError('Date of birth cannot be in the future.')
        return dob

# UserRegistrationForm with custom password and email validation
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    # Ensure the two password fields match
    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise ValidationError('The two password fields didn’t match.')
        return cd.get('password2')

    # Username validation to ensure no special characters
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError('Username can only contain letters, numbers, and underscores.')
        return username

    # Email validation to ensure the email is unique
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already in use.')
        return email
