from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.core.mail import send_mail

from .models import *

admin.site.site_url = '/account'


@admin.action(description='Ativar Contas')
def activate(modeladmin, request, queryset):
    queryset.update(is_active=True)
    for data in queryset:
        send_mail(
            subject="Você foi autorizado",
            message="http://" + request.get_host() + "/account/",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[data.username]
        )


@admin.action(description='Desativar Contas')
def disable(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.register(Conta)
class AccountAdmin(auth_admin.UserAdmin):
    list_filter = ['is_active']
    list_display = ['email', 'first_name', 'last_name', 'is_active']
    fieldsets = auth_admin.UserAdmin.fieldsets + (
        ('Campos Personalizados', {'fields': ('request_message', 'institution_name')}),
    )
    actions = [activate, disable]


@admin.register(Simulador)
class SimulatorAdmin(admin.ModelAdmin):
    list_display = ['profile', 'title', 'token']
