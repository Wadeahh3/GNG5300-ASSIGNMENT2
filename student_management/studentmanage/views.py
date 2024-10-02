from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Student
from django.urls import reverse_lazy
from .forms import StudentForm, UserRegistrationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import Http404
from django.views import View

# Student list view with pagination and search functionality
class StudentListView(ListView):
    model = Student
    template_name = 'studentmanage/student_list.html'
    context_object_name = 'students'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Student.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
        return Student.objects.all()

# View for student details, handling non-existent records
class StudentDetailView(DetailView):
    model = Student
    template_name = 'studentmanage/student_detail.html'
    context_object_name = 'student'

    def get_object(self):
        student = get_object_or_404(Student, pk=self.kwargs['pk'])  # Handle non-existent records
        return student

# View to create a new student
class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'studentmanage/student_form.html'
    success_url = reverse_lazy('studentmanage:student_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Student'
        return context

# View to update student information
class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'studentmanage/student_form.html'
    success_url = reverse_lazy('studentmanage:student_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Student Information'
        return context

# User registration view
class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'studentmanage/register.html'
    success_url = reverse_lazy('studentmanage:student_list')

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

# Function-based view for user registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('studentmanage:student_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Custom error handling and form validation
def custom_error_404(request, exception):
    return render(request, '404.html', status=404)
