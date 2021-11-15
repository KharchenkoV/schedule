from django.http import request
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.views import LoginView
from .forms import *
from django.contrib.auth import login
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
# Create your views here.

def home(request):
    return render(request, 'home.html')

class UserLoginView(LoginView):
    template_name = 'user/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')



class RegisterPage(FormView):
    template_name = 'user/register.html'
    form_class = RegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form) 