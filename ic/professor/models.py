from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Conta(AbstractUser):
    """
    Anotações:
        Alterar label_name dos fields.
    """
    request_message = models.TextField(blank=True)
    institution_name = models.CharField(blank=True, max_length=100)
    authorized = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Contas'


class Perfil(models.Model):
    """
    Anotações:
        Quais outras informações institucionais cadastrar?
    """

    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    request_message = models.TextField()
    institution_name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return self.account.username


class Simulador(models.Model):
    """
    Anotações:
        Revisar variáveis de conceitos;
        Achar tratamentos para os fields "table_dimensions" e links.
    """

    profile = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='simulators')
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
