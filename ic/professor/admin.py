from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.core.mail import send_mail

from .models import *

admin.site.site_url = '/account'


@admin.action(description='Autorizar Contas')
def authorize(modeladmin, request, queryset):
    queryset.update(account_situation="autorizado")
    for data in queryset:
        send_mail(
            subject="Você foi autorizado",
            message="http://" + request.get_host() + "/account/",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[data.username]
        )


@admin.action(description='Não autorizar Contas')
def deauthorize(modeladmin, request, queryset):
    queryset.update(account_situation="não autorizado")
    for data in queryset:
        send_mail(
            subject="Você foi autorizado",
            message=f"{data.justification_template}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[data.username]
        )


@admin.register(Conta)
class AccountAdmin(auth_admin.UserAdmin):
    list_filter = ['account_situation']
    list_display = ['email', 'first_name', 'last_name', 'account_situation']
    fieldsets = auth_admin.UserAdmin.fieldsets + (
        ('Campos Personalizados', {
            'fields': ('request_message', 'institution_name', 'account_situation', 'justification_template')
        }),
    )
    actions = [authorize, deauthorize]


@admin.register(Simulador)
class SimulatorAdmin(admin.ModelAdmin):
    list_display = ['profile', 'title', 'token']
