"""
URL configuration for energy_hub project (Main router).
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('energy_hub.urls')),
]
