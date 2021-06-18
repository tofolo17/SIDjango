# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile, Simulator

admin.site.site_url = "/account"

# Unregister the provided model admin
admin.site.unregister(User)


# Register out own model admin, based on the default UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'is_active']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'institution_name']


@admin.register(Simulator)
class SimulatorAdmin(admin.ModelAdmin):
    list_display = ['author', 'title']
