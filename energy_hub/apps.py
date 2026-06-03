"""
AppConfig for energy_hub application.
"""
from django.apps import AppConfig


class EnergyHubConfig(AppConfig):
    """Configuration for the energy_hub application."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'energy_hub'
    verbose_name = 'Energy Hub'
