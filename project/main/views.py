from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from statuses.models import Status
from transaction_types.models import Type


def view_403(request, exception=None):  # TODO: обрабатывать, логировать
    return redirect("/")


def view_404(request, exception=None):  # TODO: обрабатывать, логировать
    return redirect("/")


class SignUp(CreateView):
    form_class = UserCreationForm
    template_name = "main/forms/signup_form.html"
    extra_context = {'title': "Регистрация", "button_text": "Создать аккаунт"}

    def get_success_url(self):
        return reverse_lazy('main:index')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = "main/forms/login_form.html"
    extra_context = {'title': "Вход", "button_text": "Войти"}

    def get_success_url(self):
        return reverse_lazy('main:index')


@login_required
def settings(request):
    context = {
        "title": "Управление справочниками",
        "statuses": Status.objects.filter(created_by=request.user),
        "types": Type.objects.filter(created_by=request.user),
    }
    return render(request, 'main/settings.html', context)
