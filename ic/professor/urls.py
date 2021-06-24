from django.urls import path, include

from . import views
from .views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),  # Esconder url de register

    path('', include('django.contrib.auth.urls')),

    path('', views.SimulatorListView.as_view(), name='dashboard'),
    path('create/', views.SimulatorCreateView.as_view(), name='create'),
    path('<int:pk>', views.SimulatorDetailView.as_view(), name='detail'),
    path('<int:pk>/update', views.SimulatorUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', views.SimulatorDeleteView.as_view(), name='delete'),
    path('<int:pk>/change_token', views.change_token, name='change_token'),
]
