from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Conta(AbstractUser):
    request_message = models.TextField(blank=True, verbose_name="Mensagem de solicitação")
    institution_name = models.CharField(blank=True, max_length=100, verbose_name="Nome da instituição de ensino")

    class Meta:
        verbose_name_plural = 'Contas'


Conta._meta.get_field('email')._unique = True


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

    class Meta:
        verbose_name_plural = 'Simuladores'

    def __str__(self):
        return self.title
