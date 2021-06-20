from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .models import *

admin.site.site_url = '/account'


@admin.action(description='Autorizar Contas')
def authorize(modeladmin, request, queryset):
    queryset.update(authorized=True)


@admin.action(description='Desautorizar Contas')
def deauthorize(modeladmin, request, queryset):
    queryset.update(authorized=False)


@admin.register(Conta)
class AccountAdmin(auth_admin.UserAdmin):
    list_filter = ['authorized']
    list_display = ['email', 'first_name', 'last_name', 'authorized']
    fieldsets = auth_admin.UserAdmin.fieldsets + (
        ('Campos Personalizados', {'fields': ('request_message', 'institution_name', 'authorized')}),
    )
    actions = [authorize, deauthorize]


@admin.register(Simulador)
class SimulatorAdmin(admin.ModelAdmin):
    list_display = ['profile', 'title']
