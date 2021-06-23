from django.urls import path

from .views import simulator

urlpatterns = [
    path('simulador/<str:token>', simulator, name='simulador')
]
