from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Usuario personalizado para Energy Hub"""
    home_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

class Device(models.Model):
    """Dispositivo IoT conectado"""
    DEVICE_TYPES = [
        ('ac', 'Aire Acondicionado'),
        ('fridge', 'Refrigerador'),
        ('tv', 'Televisor'),
        ('washer', 'Lavadora'),
        ('pc', 'Computadora'),
        ('microwave', 'Microondas'),
        ('other', 'Otro'),
    ]

    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('standby', 'En Espera'),
        ('inactive', 'Inactivo'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    power_rating = models.FloatField(help_text='Potencia nominal en Watts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'devices'
        verbose_name = 'Dispositivo'
        verbose_name_plural = 'Dispositivos'

    def __str__(self):
        return f"{self.name} ({self.location})"

class EnergyReading(models.Model):
    """Lectura de consumo energético"""
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='readings')
    timestamp = models.DateTimeField(auto_now_add=True)
    voltage = models.FloatField(help_text='Voltaje en V')
    current = models.FloatField(help_text='Corriente en A')
    power = models.FloatField(help_text='Potencia en W')
    energy = models.FloatField(help_text='Energía acumulada en kWh')

    class Meta:
        db_table = 'energy_readings'
        verbose_name = 'Lectura de Energía'
        verbose_name_plural = 'Lecturas de Energía'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.device.name} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class Alert(models.Model):
    """Alerta del sistema"""
    SEVERITY_CHOICES = [
        ('critical', 'Crítica'),
        ('high', 'Alta'),
        ('medium', 'Media'),
        ('low', 'Baja'),
    ]

    TYPE_CHOICES = [
        ('consumption', 'Consumo Excesivo'),
        ('standby', 'Consumo Fantasma'),
        ('anomaly', 'Anomalía Detectada'),
        ('threshold', 'Umbral Superado'),
        ('device', 'Dispositivo Offline'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='alerts', null=True, blank=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    alert_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'alerts'
        verbose_name = 'Alerta'
        verbose_name_plural = 'Alertas'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.severity})"
