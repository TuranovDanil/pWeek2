from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegisterUserForm
from .models import Request


def index(request):
    counter = Request.objects.filter(status="work").all().count()
    rec = Request.objects.filter(status="completed")[:4]
    return render(request, 'main/index.html', {'rec': rec, 'counter': counter})


class BBLoginView(LoginView):
    template_name = 'main/login.html'


@login_required
def profile(request):
    return render(request, 'main/profile.html')


class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


class RegisterViews(CreateView):
    template_name = 'main/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:login')
