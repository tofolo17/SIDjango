import secrets

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Conta(AbstractUser):
    """
    Anotações:
        Há outras informações a serem estendidas?
    """
    request_message = models.TextField(blank=True, verbose_name="Mensagem de solicitação")
    institution_name = models.CharField(blank=True, max_length=100, verbose_name="Nome da instituição de ensino")

    class Meta:
        verbose_name_plural = 'Contas'


Conta._meta.get_field('email')._unique = True


def get_token():
    return secrets.token_urlsafe(16)


class Simulador(models.Model):
    """
    Anotações:
        Revisar variáveis de conceitos;
        Achar tratamentos para os fields "table_dimensions" e links.
    """

    profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)

    required_concepts = models.CharField(max_length=250)
    minimum_concepts = models.CharField(max_length=250)

    table_dimensions = models.CharField(max_length=100)

    youtube_link = models.CharField(max_length=250)
    form_link = models.CharField(max_length=250)

    updated = models.DateTimeField(auto_now=True)
    token = models.TextField(max_length=16, default=get_token, unique=True)

    class Meta:
        verbose_name_plural = 'Simuladores'

    def __str__(self):
        return self.title
