from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Student
from django.urls import reverse_lazy
from .forms import StudentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.views import View
from django.db.models import Q



class StudentListView(ListView):
    model = Student
    template_name = 'studentmanage/student_list.html'
    context_object_name = 'students'
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Student.objects.filter(first_name__icontains=query) | Student.objects.filter(last_name__icontains=query)
        else:
            return Student.objects.all()

class StudentDetailView(DetailView):
    model = Student
    template_name = 'studentmanage/student_detail.html'
    context_object_name = 'student'

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'studentmanage/student_form.html'
    success_url = reverse_lazy('studentmanage:student_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'add new students'
        return context

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'studentmanage/student_form.html'
    success_url = reverse_lazy('studentmanage:student_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'edit student information'
        return context
    
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