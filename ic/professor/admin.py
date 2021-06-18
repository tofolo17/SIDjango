from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .models import *

admin.site.site_url = "/account"

admin.site.register(Conta, auth_admin.UserAdmin)


@admin.register(Perfil)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['account', 'institution_name']


@admin.register(Simulador)
class SimulatorAdmin(admin.ModelAdmin):
    list_display = ['profile', 'title']
