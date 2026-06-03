from django.contrib import admin
from .models import User, Device, EnergyReading, Alert

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'home_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'home_name')
    ordering = ('-date_joined',)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'device_type', 'location', 'status', 'user', 'created_at')
    list_filter = ('device_type', 'status', 'location')
    search_fields = ('name', 'location', 'user__username')
    ordering = ('-created_at',)

@admin.register(EnergyReading)
class EnergyReadingAdmin(admin.ModelAdmin):
    list_display = ('device', 'timestamp', 'voltage', 'current', 'power', 'energy')
    list_filter = ('device', 'timestamp')
    search_fields = ('device__name',)
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'severity', 'alert_type', 'user', 'device', 'is_resolved', 'created_at')
    list_filter = ('severity', 'alert_type', 'is_resolved', 'created_at')
    search_fields = ('title', 'message', 'user__username', 'device__name')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    actions = ['mark_as_resolved']

    def mark_as_resolved(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_resolved=True, resolved_at=timezone.now())
    mark_as_resolved.short_description = "Marcar alertas seleccionadas como resueltas"
