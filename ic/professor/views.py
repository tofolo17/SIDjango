from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .forms import UserRegistrationForm, LoginForm
from .models import Simulador


@method_decorator(login_required, name='dispatch')
class SimulatorListView(ListView):
    model = Simulador
    template_name = 'account/dashboard.html'
    context_object_name = 'simulators'

    def get_context_data(self, **kwargs):
        context = super(SimulatorListView, self).get_context_data(**kwargs)
        simulators = self.get_queryset().filter(profile_id=self.request.user.id)
        context['simulators'] = simulators
        return context


@method_decorator(login_required, name='dispatch')
class SimulatorDetailView(DetailView):
    model = Simulador
    template_name = 'account/detail.html'
    context_object_name = 'simulator'


@method_decorator(login_required, name='dispatch')
class SimulatorCreateView(CreateView):
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

    def form_valid(self, form):
        form.instance.profile = self.request.user
        return super(SimulatorCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class SimulatorUpdateView(UpdateView):
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

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'pk': self.object.id})


@method_decorator(login_required, name='dispatch')
class SimulatorDeleteView(DeleteView):
    model = Simulador
    template_name = 'account/delete.html'
    success_url = reverse_lazy('dashboard')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)

            new_user.is_active = False
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
