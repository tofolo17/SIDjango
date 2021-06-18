from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.forms import UserCreationForm

from .models import *

admin.site.site_url = '/account'


@admin.register(Conta)
class AccountAdmin(auth_admin.UserAdmin):
    """
    Anotações:
        Alterar filtros, barra de pesquisa e afins
    """
    list_display = ['email', 'first_name', 'last_name', 'authorized']
    form = UserCreationForm
    model = Conta
    fieldsets = auth_admin.UserAdmin.fieldsets + (
        ('Campos Personalizados', {'fields': ('request_message', 'institution_name', 'authorized')}),
    )


@admin.register(Perfil)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['account', 'institution_name']


@admin.register(Simulador)
class SimulatorAdmin(admin.ModelAdmin):
    list_display = ['profile', 'title']
