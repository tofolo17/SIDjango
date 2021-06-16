# Register your models here.

from django.contrib import admin

from .models import Profile, Simulator


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'institution_name']


@admin.register(Simulator)
class SimulatorAdmin(admin.ModelAdmin):
    list_display = ['author', 'title']