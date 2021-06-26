from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .forms import UserRegistrationForm, LoginForm
from .models import Simulador, get_token


class SimulatorListView(LoginRequiredMixin, ListView):
    model = Simulador
    template_name = 'account/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(SimulatorListView, self).get_context_data(**kwargs)
        simulators = self.get_queryset().filter(profile_id=self.request.user.id).order_by('-updated')
        context['simulators'] = simulators
        return context


class SimulatorDetailView(LoginRequiredMixin, DetailView):
    model = Simulador
    template_name = 'account/detail.html'
    context_object_name = 'simulator'

    def get_queryset(self):
        qs = super(SimulatorDetailView, self).get_queryset().filter(profile_id=self.request.user.id)
        return qs


class SimulatorCreateView(LoginRequiredMixin, CreateView):
    """
    Anotações:
        Terminar método de limite
            https://stackoverflow.com/questions/59462964/django-createview-only-allow-n-number-of-objects-created-redirect-if-limit-is
    """
    model = Simulador
    template_name = 'account/create.html'
    fields = (
        'title',
        'required_concepts',
        'minimum_concepts',
        'table_dimensions',
        'youtube_link',
        'form_link'
    )
    success_url = reverse_lazy('dashboard')

    def is_limit_reached(self):
        pass

    def form_valid(self, form):
        form.instance.profile = self.request.user
        return super(SimulatorCreateView, self).form_valid(form)


class SimulatorUpdateView(LoginRequiredMixin, UpdateView):
    model = Simulador
    template_name = 'account/update.html'
    fields = (
        'title',
        'required_concepts',
        'minimum_concepts',
        'table_dimensions',
        'youtube_link',
        'form_link'
    )

    def get_queryset(self):
        qs = super(SimulatorUpdateView, self).get_queryset().filter(profile_id=self.request.user.id)
        return qs

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'pk': self.object.id})


class SimulatorDeleteView(LoginRequiredMixin, DeleteView):
    model = Simulador
    template_name = 'account/delete.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        qs = super(SimulatorDeleteView, self).get_queryset().filter(profile_id=self.request.user.id)
        return qs


@login_required()
def update_token(request, pk):
    status = None
    simulator = get_object_or_404(Simulador, profile_id=request.user.id, pk=pk)
    if request.method == 'POST':
        simulator.token = get_token()
        simulator.save()
        status = "Ok"
    return render(
        request,
        'account/change_token.html',
        {
            'simulator': simulator,
            'status': status
        }
    )


def access_simulator(request, token):
    simulator = get_object_or_404(Simulador, token=token)
    return render(
        request,
        'simulator/simulator.html',
        {'simulator': simulator}
    )


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.username = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']
            try:
                validate_password(password, new_user)
                new_user.set_password(password)
                new_user.save()

                send_mail(
                    subject="Nova requisição de uso",
                    message="http://" + request.get_host() + "/admin/",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.ADMIN_MAIL]
                )

                return render(
                    request,
                    'account/register_done.html',
                    {'new_user': new_user}
                )
            except ValidationError as e:
                user_form.add_error('password', e)
    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        'account/register.html',
        {'user_form': user_form}
    )


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'
