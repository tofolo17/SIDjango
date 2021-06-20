from django.urls import path, include

from . import views
from .views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),

    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),

    path('register/', views.register, name='register')
]
