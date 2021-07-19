from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.password_validation import validate_password
from django.contrib.postgres.search import TrigramSimilarity
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from taggit.models import Tag

from .forms import UserRegistrationForm, LoginForm, CreateViewForm
from .models import Simulador, get_token, Conta


# Class-based views para Simulador
class SimulatorListView(LoginRequiredMixin, ListView):
    model = Simulador
    context_object_name = 'simulators'
    template_name = 'simulator/dashboard.html'
    extra_context = {'active': 'dashboard'}

    def get_queryset(self, **kwargs):
        simulators = Simulador.objects.filter(profile_id=self.request.user.id).order_by('-updated')
        return simulators


class SimulatorCreateView(LoginRequiredMixin, CreateView):
    form_class = CreateViewForm
    template_name = 'simulator/create.html'
    success_url = reverse_lazy('dashboard')
    tags = [tag for tag in Tag.objects.all()]
    tags_to_tagify = ','.join([str(i) for i in tags])
    extra_context = {
        'tags': tags_to_tagify
    }

    def get_form_kwargs(self):
        kwargs = super(SimulatorCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.instance.profile = self.request.user
        return super(SimulatorCreateView, self).form_valid(form)


class SimulatorUpdateView(LoginRequiredMixin, UpdateView):
    model = Simulador
    template_name = 'simulator/update.html'
    fields = (
        'title',
        'tags',
        'required_concepts',
        'minimum_concepts',
        'table_dimensions',
        'youtube_link',
        'form_link',
        'private',
        'token'
    )
    success_url = '/account/updated/'
    tags = [tag for tag in Tag.objects.all()]
    tags_to_tagify = ','.join([str(i) for i in tags])
    extra_context = {
        'tags': tags_to_tagify
    }

    def get_queryset(self):
        qs = super(SimulatorUpdateView, self).get_queryset().filter(profile_id=self.request.user.id)
        return qs


class SimulatorDeleteView(LoginRequiredMixin, DeleteView):
    model = Simulador
    template_name = 'simulator/delete.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        qs = super(SimulatorDeleteView, self).get_queryset().filter(profile_id=self.request.user.id)
        return qs

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        finally:
            Tag.objects.annotate(
                ntag=Count('taggit_taggeditem_items')
            ).filter(ntag=0).delete()


class ExploreSimulatorListView(ListView):
    model = Simulador
    template_name = 'simulator/explore.html'
    context_object_name = 'simulators'
    extra_context = {
        'active': 'explore'
    }

    def get_context_data(self, **kwargs):
        context = super(ExploreSimulatorListView, self).get_context_data(**kwargs)

        # Parâmetros via GET da URL
        sim_q = self.request.GET.get('q')
        tag_q = self.request.GET.get('q2')

        # Tratamento da query do simulador
        if not sim_q:
            simulators = self.get_queryset().filter(private=False)
        else:
            simulators = Simulador.objects.annotate(
                similarity=TrigramSimilarity('title', sim_q)
            ).filter(similarity__gt=0.1).order_by('-similarity')
            context['sim_q'] = True
        try:
            if self.kwargs['tag'] is not None:
                my_tags = Tag.objects.filter(slug=self.kwargs['tag']).values_list('name', flat=True)
                simulators = simulators.filter(tags__name__in=my_tags)
                context['tag_name'] = [tag for tag in my_tags][0]
        except Exception:
            pass

        # Tratamento da query dos marcadores
        if not tag_q:
            tags = Tag.objects.all()
        else:
            tags = Tag.objects.annotate(
                similarity=TrigramSimilarity('name', tag_q)
            ).filter(similarity__gt=0.1).order_by('-similarity')
            context['tag_q'] = True

        context['simulators'] = simulators
        context['tags'] = tags
        return context


class ExploreSimulatorUpdateView(UpdateView):
    model = Simulador
    template_name = 'simulator/details.html'
    fields = (
        'title',
        'tags',
        'required_concepts',
        'minimum_concepts',
        'table_dimensions'
    )


# Normal views para Simulador
@login_required()
def update_token(request, pk):
    simulator = get_object_or_404(Simulador, profile_id=request.user.id, pk=pk)
    if request.method == 'POST':
        simulator.token = get_token()
        simulator.save()
        return render(request, 'account/updated.html', {'token': simulator.token})
    return render(
        request,
        'simulator/change_token.html',
        {
            'simulator': simulator,
        }
    )


def access_simulator(request, token):
    simulator = get_object_or_404(Simulador, token=token)
    return render(
        request,
        'simulator/simulator.html',
        {'simulator': simulator}
    )


# Class-based views para Conta
class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Conta
    template_name = 'account/update.html'
    fields = (
        'first_name',
        'last_name',
        'request_message',
        'institution_name'
    )
    success_url = '/account/updated/'
    extra_context = {'active': 'profile'}

    def get_queryset(self):
        qs = super(AccountUpdateView, self).get_queryset().filter(id=self.request.user.id)
        return qs


# Class-based auth views para Conta
class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'
    extra_context = {'active': 'login'}


# Normal auth views para Conta
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
        {
            'user_form': user_form,
            'active': 'register'
        }
    )


# Normal views para Conta
@login_required()
def updated(request):
    return render(request, 'account/updated.html')
