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
        Tags
            https://stackoverflow.com/questions/48086513/django-taggit-display-existing-tags-on-the-django-admin-add-record-page
    """
    tags = TaggableManager()

    profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)

    required_concepts = models.CharField(max_length=250)
    minimum_concepts = models.CharField(max_length=250)

    table_dimensions = models.CharField(max_length=100)

    youtube_link = models.CharField(max_length=250)
    form_link = models.CharField(max_length=250)

    updated = models.DateTimeField(auto_now=True)
    token = models.TextField(max_length=16, default=get_token, unique=True)

    private = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Simuladores'

    def __str__(self):
        return self.title
