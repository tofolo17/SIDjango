# Create your models here.
from django.contrib.auth.models import User
from django.db import models

"""
Texto grande: 500
Texto médio: 250
Texto pequeno: 100
"""

# TODO: Como utilizar a classe Meta? Criar campo de updated pros simuladores?


User._meta.get_field('username')._unique = True  # Ideal: no cadastro, username = email.
User._meta.get_field('email')._unique = True


class Profile(models.Model):
    # Usuário
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Mensagem de solicitação de uso
    request_message = models.TextField()

    # Informações da instituição de ensino
    institution_name = models.CharField(max_length=100)  # TODO: Cadastrar outras informações da instituição (quais?)

    def __str__(self):
        return self.user.username


class Simulator(models.Model):
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
