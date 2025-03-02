from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages  # Para mostrar mensajes en la interfaz
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages


User = get_user_model()  # Obtener el modelo de usuario personalizado

def registro_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        apellido2 = request.POST.get("apellido2", "")
        email = request.POST.get("email")
        num_tel = request.POST.get("num_tel")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Validaciones
        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está registrado.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "El correo ya está registrado.")
        else:
            # Crear usuario con el modelo personalizado
            user = User.objects.create_user(
                username=username,
                first_name=nombre,
                last_name=apellido,
                email=email,
                password=password1
            )
            user.apellido2 = apellido2  # Guardar segundo apellido
            user.num_tel = num_tel  # Guardar teléfono
            user.save()

            messages.success(request, "Cuenta creada exitosamente. Ahora puedes iniciar sesión.")
            return redirect("login")  # Redirigir al login tras registro exitoso

    return render(request, "registro.html")

# 🔹 Página de inicio
def inicio(request):
    return render(request, "inicio.html")

# 🔹 Páginas informativas
def reseñas(request):
    return render(request, "reseñas.html")

def pedidos(request):
    return render(request, "pedidos.html")

def Tienda(request):
    return render(request, "Tienda.html")

def faq(request):
    return render(request, "faq.html")

User = get_user_model()  # Obtener el modelo de usuario personalizado

User = get_user_model()

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No existe una cuenta con ese correo electrónico.")
            return render(request, "login.html")

        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "Inicio de sesión exitoso.")
                return redirect("inicio")  # Redirige a la página principal
            else:
                messages.error(request, "Tu cuenta está inactiva. Contacta con soporte.")
        else:
            messages.error(request, "Correo o contraseña incorrectos.")

    return render(request, "login.html")  # Siempre muestra la página de login


User = get_user_model()

def registro_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        apellido2 = request.POST.get("apellido2", "")
        email = request.POST.get("email")
        num_tel = request.POST.get("num_tel", "")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        cuenta_bancaria = request.POST.get("cuenta_bancaria", "")
        direccion = request.POST.get("direccion", "")

        # Validaciones
        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está registrado.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "El correo ya está registrado.")
        else:
            # Crear usuario
            user = User.objects.create_user(
                username=username,
                first_name=nombre,
                last_name=apellido,
                email=email,
                password=password1
            )
            user.apellido2 = apellido2  # Guardar segundo apellido
            user.num_tel = num_tel  # Guardar teléfono
            user.cuenta_bancaria = cuenta_bancaria  # Guardar cuenta bancaria
            user.direccion = direccion  # Guardar dirección
            user.save()

            messages.success(request, "Cuenta creada exitosamente. Ahora puedes iniciar sesión.")
            return redirect("login")  # Redirigir al login tras registro exitoso

    return render(request, "registro.html")

#  Página de perfil (puede necesitar ajustes)
def perfil(request):
    return render(request, "perfil.html")

#  Logout para cerrar sesión
def logout_view(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect("login")

#  Configurar recuperación de contraseña con Django
from django.contrib.auth import views as auth_views

class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = "password_reset.html"
