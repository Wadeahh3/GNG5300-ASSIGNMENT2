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
    fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'enrollment_date', 'grade']
    template_name = 'studentmanage/student_form.html'
    success_url = reverse_lazy('studentmanage:student_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'add new students'
        return context

class StudentUpdateView(UpdateView):
    model = Student
    fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'enrollment_date', 'grade']
    template_name = 'studentmanage/student_form.html'
    success_url = reverse_lazy('studentmanage:student_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'edit student information'
        return context
