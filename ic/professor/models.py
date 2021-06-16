# Create your models here.
from django.conf import settings
from django.db import models

"""
Texto grande: 500
Texto médio: 250
Texto pequeno: 100
"""


class Profile(models.Model):
    # Usuário
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Mensagem de solicitação de uso
    request_message = models.TextField()

    # Informações da instituição de ensino
    institution_name = models.CharField(max_length=100)  # TODO: Cadastrar outras informações da instituição (quais?)

    def __str__(self):
        return self.user.username


class Simulator(models.Model):  # Devo criar campo para data?
    # Criador do simulador
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='simulators')

    # Variáveis do simulador
    title = models.CharField(max_length=100)

    required_concepts = models.CharField(max_length=250)
    minimum_concepts = models.CharField(max_length=250)  # TODO: Revisar variáveis de conceitos

    table_dimensions = models.CharField(max_length=100)

    youtube_link = models.CharField(max_length=250)
    form_link = models.CharField(max_length=250)

    # TODO: Tentar achar field type adequado para "table_dimensions" e links

    def __str__(self):
        return self.title
