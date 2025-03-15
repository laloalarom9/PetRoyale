from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages  # Para mostrar mensajes en la interfaz
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from mi_proyecto.models import CustomUser
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Producto
from .forms import ProductoForm
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse



User = get_user_model()  # Obtener el modelo de usuario personalizado

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
        genero = request.POST.get("genero", "")
        cuenta_bancaria = request.POST.get("cuenta_bancaria", "")
        direccion = request.POST.get("direccion", "")

        # 🔍 DEPURACIÓN: IMPRIMIR VALORES RECIBIDOS
        print(f"DEBUG: num_tel={num_tel} (longitud={len(num_tel)})")

        # Validación para evitar el error
        if len(num_tel) > 15:
            messages.error(request, "El número de teléfono no puede tener más de 15 caracteres.")
            return render(request, "registro.html", {
                "username": username,
                "nombre": nombre,
                "apellido": apellido,
                "apellido2": apellido2,
                "email": email,
                "num_tel": num_tel,
                "genero": genero,
                "cuenta_bancaria": cuenta_bancaria,
                "direccion": direccion,
            })

        # Validaciones generales
        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
        elif User.objects.filter(email__iexact=email).exists():
            messages.error(request, "El correo ya está registrado. Usa otro o inicia sesión.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está registrado.")
        else:
            # Crear usuario
            user = User.objects.create_user(
                username=username,
                first_name=nombre,
                last_name=apellido,
                email=email,
                password=password1,
            )
            user.apellido2 = apellido2
            user.num_tel = num_tel
            user.genero = genero
            user.cuenta_bancaria = cuenta_bancaria
            user.direccion = direccion
            user.save()

            messages.success(request, "Cuenta creada exitosamente. Ahora puedes iniciar sesión.")
            return redirect("login")

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


def login_view(request):
    messages.get_messages(request).used = True  # 🔹 Borra mensajes anteriores

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)  # Buscar usuario por email
        except User.DoesNotExist:
            messages.error(request, "No existe una cuenta con este correo electrónico.")
            return render(request, "login.html")

        user_authenticated = authenticate(request, username=user.username, password=password)

        if user_authenticated is not None:
            if user_authenticated.is_active:
                login(request, user_authenticated)
                messages.success(request, "Inicio de sesión exitoso.")
                return redirect("inicio")  # Redirige a la página principal
            else:
                messages.error(request, "Tu cuenta está inactiva. Contacta con soporte.")
        else:
            messages.error(request, "La contraseña es incorrecta.")  #  Mensaje específico para contraseña incorrecta

    return render(request, "login.html")  # Siempre renderiza la página de login en caso de error


from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def eliminar_cuenta(request):
    user = request.user
    user.delete()
    messages.success(request, "Tu cuenta ha sido eliminada correctamente.")
    return redirect("inicio")  # Redirige a la página de inicio después de eliminar la cuenta

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
        genero = request.POST.get("genero", "hombre")  # Si no envía nada, por defecto será "hombre"
        cuenta_bancaria = request.POST.get("cuenta_bancaria", "")
        direccion = request.POST.get("direccion", "")

        print(f"DEBUG - Género recibido: {genero}")  # 🔍 Para ver qué se está recibiendo

        # Validaciones
        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
        elif User.objects.filter(email__iexact=email).exists():
            messages.error(request, "El correo ya está registrado. Usa otro o inicia sesión.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está registrado.")
        else:
            # Crear usuario sin el campo `genero`
            user = User.objects.create_user(
                username=username,
                first_name=nombre,
                last_name=apellido,
                email=email,
                password=password1
            )

            # Asignar el género correctamente después de la creación
            user.apellido2 = apellido2
            user.num_tel = num_tel
            user.genero = genero  # 🔹 Aquí se asigna correctamente el género
            user.cuenta_bancaria = cuenta_bancaria
            user.direccion = direccion
            user.save()  # 🔹 Guardar el usuario con el género actualizado

            messages.success(request, "Cuenta creada exitosamente. Ahora puedes iniciar sesión.")
            return redirect("login")  # Redirigir al login tras registro exitoso

        # Si hay un error, recargar la página con los datos ingresados
        return render(request, "registro.html", {
            "username": username,
            "nombre": nombre,
            "apellido": apellido,
            "apellido2": apellido2,
            "email": email,
            "num_tel": num_tel,
            "genero": genero,
            "cuenta_bancaria": cuenta_bancaria,
            "direccion": direccion,
        })

    return render(request, "registro.html")


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from mi_proyecto.models import CustomUser

@login_required
def editar_perfil(request):
    user = request.user  # Usuario autenticado

    if request.method == "POST":
        user.email = request.POST.get("email", user.email)
        user.first_name = request.POST.get("first_name", "")
        user.last_name = request.POST.get("last_name", "")
        user.apellido2 = request.POST.get("apellido2", "")
        user.num_tel = request.POST.get("num_tel", "")
        user.genero = request.POST.get("genero", "hombre")  # Si no elige nada, se mantiene "hombre" como default

        # Manejo de contraseña: solo la cambia si ambas coinciden y no están vacías
        password = request.POST.get("password", "")
        password_confirm = request.POST.get("password_confirm", "")

        if password and password == password_confirm:
            user.password = make_password(password)
        elif password and password != password_confirm:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect("perfil")

        user.save()
        messages.success(request, "Perfil actualizado correctamente.")
        return redirect("perfil")  # Redirige a la misma página de perfil

    return render(request, "perfil.html", {"user": user})

#  Logout para cerrar sesión
def logout_view(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect("login")

#  Configurar recuperación de contraseña con Django
from django.contrib.auth import views as auth_views

class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = "password_reset.html"

def es_superusuario(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(es_superusuario)
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto agregado correctamente.")
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'agregar_producto.html', {'form': form})

def mostrar_imagen_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if producto.imagen:
        return HttpResponse(producto.imagen, content_type="image/jpeg")
    else:
        return HttpResponse(status=404)
    
@user_passes_test(es_superusuario)
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'admin_productos.html', {'productos': productos})

@user_passes_test(es_superusuario)
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})

@user_passes_test(es_superusuario)
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    messages.success(request, "Producto eliminado correctamente.")
    return redirect('lista_productos')

def Tienda(request):
    productos = Producto.objects.all()  # Obtener todos los productos
    return render(request, "Tienda.html", {"productos": productos})