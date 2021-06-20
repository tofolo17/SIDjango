from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .models import *

admin.site.site_url = '/account'


@admin.register(Conta)
class AccountAdmin(auth_admin.UserAdmin):
    """
    Anotações:
        Adicionar filtros por autorizado e afins.
    """
    list_display = ['email', 'first_name', 'last_name', 'authorized']
    fieldsets = auth_admin.UserAdmin.fieldsets + (
        ('Campos Personalizados', {'fields': ('request_message', 'institution_name', 'authorized')}),
    )


@admin.register(Simulador)
class SimulatorAdmin(admin.ModelAdmin):
    list_display = ['profile', 'title']
