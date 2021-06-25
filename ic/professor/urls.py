from django.urls import path, include

from . import views
from .views import LoginView

urlpatterns = [
    path('account/login/', LoginView.as_view(), name='login'),
    path('account/register/', views.register, name='register'),

    path('account/', include('django.contrib.auth.urls')),

    path('account/', views.SimulatorListView.as_view(), name='dashboard'),
    path('account/create/', views.SimulatorCreateView.as_view(), name='create'),
    path('account/<int:pk>', views.SimulatorDetailView.as_view(), name='detail'),
    path('account/<int:pk>/update', views.SimulatorUpdateView.as_view(), name='update'),
    path('account/<int:pk>/delete', views.SimulatorDeleteView.as_view(), name='delete'),
    path('account/<int:pk>/update_token', views.update_token, name='change_token'),

    path('simulator/<str:token>', views.access_simulator, name='simulator')
]
