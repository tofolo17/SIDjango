import secrets

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from taggit.managers import TaggableManager


class Conta(AbstractUser):
    """
    Anotações:
        Informações a serem estendidas
            CPF
            RG
            Nome da mãe
    """
    SITUATION_CHOICES = (
        ('autorizado', 'Autorizado'),
        ('pendente', 'Pendente'),
        ('não autorizado', 'Não autorizado')
    )

    request_message = models.TextField(
        verbose_name="Mensagem de solicitação",
        help_text="Use este campo para informar os seus objetivos de uso, metas de aprendizado, e afins."
    )
    institution_name = models.CharField(max_length=100, verbose_name="Instituição de ensino")
    account_situation = models.CharField(max_length=15, choices=SITUATION_CHOICES, default='pendente')
    justification_template = models.TextField(
        verbose_name="Justificativa para não autorização",
        default="Desculpe, mas seu pedido foi negado."
    )

    class Meta:
        verbose_name_plural = 'Contas'


Conta._meta.get_field('email')._unique = True


def get_token():
    return secrets.token_urlsafe(12)


class Simulador(models.Model):
    """
    Anotações:
        Achar tratamentos para os fields "table_dimensions" e links.
    """
    tags = TaggableManager()

    profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(
        max_length=100,
        verbose_name="Título"
    )

    required_concepts = models.CharField(
        max_length=250,
        verbose_name="Conceitos necessários"
    )
    minimum_concepts = models.CharField(
        max_length=250,
        verbose_name="Conceitos mínimos"
    )

    table_dimensions = models.CharField(
        max_length=100,
        verbose_name="Dimensões do experimento"
    )

    youtube_link = models.CharField(
        max_length=250,
        verbose_name="Link do vídeo Youtube do experimento"
    )
    form_link = models.CharField(
        max_length=250,
        verbose_name="Link do Formulário Google"
    )

    updated = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=16, default=get_token, unique=True)

    private = models.BooleanField(
        default=True,
        verbose_name="Privado"
    )

    class Meta:
        verbose_name_plural = 'Simuladores'

    def __str__(self):
        return self.title
