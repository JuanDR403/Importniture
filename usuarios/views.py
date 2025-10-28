from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, LoginForm
from .models import Usuario


def register_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Create Django User first
            user = form.save()
            # Create corresponding entry in custom usuarios table
            nombre = form.cleaned_data.get('first_name')
            apellido = form.cleaned_data.get('last_name')
            correo = form.cleaned_data.get('email')
            telefono = form.cleaned_data.get('telefono')
            Usuario.objects.create(
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                telefono=telefono,
                idrol=1,
            )
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Has iniciado sesión correctamente.')
                return redirect('home')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})


@login_required
def home_view(request):
    return render(request, 'home.html')
