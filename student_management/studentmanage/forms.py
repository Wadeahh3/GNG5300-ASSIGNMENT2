import re
from django import forms
from .models import Student

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
