"""
Authentication views for energy_hub project.
Maneja login, registro, recuperación de contraseña y logout.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from energy_hub.models import User


def redirect_to_login(request):
    """Redirect root URL to login page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso')
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciales incorrectas')

    return render(request, 'auth/login.html')


def register_view(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        home_name = request.POST.get('home_name')

        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'auth/register.html')

        # Check if user already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado')
            return render(request, 'auth/register.html')

        # Create user
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )
            user.home_name = home_name
            user.save()
            messages.success(request, 'Cuenta creada correctamente. Por favor inicia sesión.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error al crear la cuenta: {str(e)}')

    return render(request, 'auth/register.html')


def password_recovery_view(request):
    """Handle password recovery"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    email_sent = False
    if request.method == 'POST':
        email = request.POST.get('email')
        # In production, send actual email here
        email_sent = True
        messages.success(request, 'Correo de recuperación enviado')

    return render(request, 'auth/password_recovery.html', {'email_sent': email_sent})


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente')
    return redirect('login')
