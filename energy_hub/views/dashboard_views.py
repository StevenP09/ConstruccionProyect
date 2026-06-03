"""
Dashboard views for energy_hub project.
Renderiza las vistas del dashboard, monitoreo, dispositivos, consumo, etc.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def dashboard_view(request):
    """Dashboard view"""
    return render(request, 'dashboard/dashboard.html')


@login_required
def monitoring_view(request):
    """Real-time monitoring view"""
    return render(request, 'dashboard/monitoring.html')


@login_required
def devices_view(request):
    """Devices management view"""
    return render(request, 'dashboard/devices.html')


@login_required
def consumption_view(request):
    """Consumption and costs view"""
    return render(request, 'dashboard/consumption.html')


@login_required
def alerts_view(request):
    """Alerts view"""
    return render(request, 'dashboard/alerts.html')


@login_required
def comparison_view(request):
    """Energy comparison view"""
    return render(request, 'dashboard/comparison.html')


@login_required
def recommendations_view(request):
    """AI recommendations view"""
    return render(request, 'dashboard/recommendations.html')


@login_required
def profile_view(request):
    """User profile view"""
    if request.method == 'POST':
        # Handle profile update
        request.user.first_name = request.POST.get('name', request.user.first_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()
        messages.success(request, 'Perfil actualizado correctamente')

    return render(request, 'dashboard/profile.html')
