"""
Observer Pattern (Signals)
Implementa el patrón Observer usando Django Signals.
Usado para alertas y monitoreo en tiempo real.
"""
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.signals import Signal


# Señales personalizadas
alert_triggered = Signal()
consumption_updated = Signal()
device_status_changed = Signal()


# Receptores de señales (Observers)
# Ejemplo:
# @receiver(post_save, sender=EnergyReading)
# def energy_reading_created(sender, instance, created, **kwargs):
#     """Se dispara cuando se crea una nueva lectura de energía"""
#     if created:
#         # Verificar si debe generar alertas
#         alert_triggered.send(sender=sender, reading=instance)


class AlertObserver:
    """
    Observador que escucha cambios en los datos de energía
    y genera alertas si es necesario.
    Patrón: Observer
    """

    @staticmethod
    def notify_alert(sender, **kwargs):
        """
        Notifica cuando se dispara una alerta.
        """
        # Implementación futura
        pass


class MonitoringObserver:
    """
    Observador que escucha cambios en tiempo real
    para actualizar el monitoreo.
    Patrón: Observer
    """

    @staticmethod
    def notify_monitoring_update(sender, **kwargs):
        """
        Notifica sobre actualizaciones de monitoreo en tiempo real.
        """
        # Implementación futura
        pass
