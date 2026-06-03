"""
URL configuration for energy_hub app.
Rutas específicas de la aplicación energy_hub.
"""
from django.urls import path
from energy_hub.views.auth_views import (
    redirect_to_login,
    login_view,
    register_view,
    password_recovery_view,
    logout_view,
)
from energy_hub.views.dashboard_views import (
    dashboard_view,
    monitoring_view,
    devices_view,
    consumption_view,
    alerts_view,
    comparison_view,
    recommendations_view,
    profile_view,
)

urlpatterns = [
    # Authentication URLs
    path('', redirect_to_login, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('recovery/', password_recovery_view, name='password_recovery'),
    path('logout/', logout_view, name='logout'),

    # Dashboard URLs
    path('dashboard/', dashboard_view, name='dashboard'),
    path('monitoring/', monitoring_view, name='monitoring'),
    path('devices/', devices_view, name='devices'),
    path('consumption/', consumption_view, name='consumption'),
    path('alerts/', alerts_view, name='alerts'),
    path('comparison/', comparison_view, name='comparison'),
    path('recommendations/', recommendations_view, name='recommendations'),
    path('profile/', profile_view, name='profile'),
]
