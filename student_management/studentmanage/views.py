from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Student
from django.urls import reverse_lazy

class StudentListView(ListView):
    model = Student
    template_name = 'studentmanage/student_list.html'
    context_object_name = 'students'

class StudentDetailView(DetailView):
    model = Student
    template_name = 'studentmanage/student_detail.html'
    context_object_name = 'student'

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm  
    template_name = 'studentmanage/student_form.html'
    success_url = reverse_lazy('studentmanage:student_list')

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm  
    template_name = 'studentmanage/student_form.html'
    success_url = reverse_lazy('studentmanage:student_list')
