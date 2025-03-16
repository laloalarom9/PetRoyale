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
from decimal import Decimal
import pprint
from django.utils.timezone import now, timedelta



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
    productos = Producto.objects.all()  # Obtener todos los productos

    # Obtener valores de los filtros de la URL
    categoria = request.GET.get("categoria", "")
    marca = request.GET.get("marca", "")
    min_precio = request.GET.get("min_precio", "")
    max_precio = request.GET.get("max_precio", "")
    edad = request.GET.get("edad_recomendada", "")
    tamano = request.GET.get("tamano_mascota", "")

    # Aplicar filtros dinámicamente
    if categoria:
        productos = productos.filter(categoria=categoria)
    if marca:
        productos = productos.filter(marca=marca)
    if min_precio:
        productos = productos.filter(precio__gte=min_precio)
    if max_precio:
        productos = productos.filter(precio__lte=max_precio)
    if edad:
        productos = productos.filter(edad_recomendada=edad)
    if tamano:
        productos = productos.filter(tamano_mascota=tamano)

    # 🔹 Obtener opciones dinámicas de la base de datos para los filtros
    categorias_disponibles = Producto.objects.values_list("categoria", flat=True).distinct()
    marcas_disponibles = Producto.objects.values_list("marca", flat=True).distinct()
    edades_disponibles = Producto.objects.values_list("edad_recomendada", flat=True).distinct()
    tamanos_disponibles = Producto.objects.values_list("tamano_mascota", flat=True).distinct()

    return render(
        request,
        "Tienda.html",
        {
            "productos": productos,
            "categorias_disponibles": categorias_disponibles,
            "marcas_disponibles": marcas_disponibles,
            "edades_disponibles": edades_disponibles,
            "tamanos_disponibles": tamanos_disponibles,
        },
    )
def faq(request):
    return render(request, "faq.html")  # Asegúrate de que tienes el archivo "faq.html"


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
            # Mostrar mensaje de error si el producto ya existe
            messages.error(request, "Error al agregar el producto. Verifica los datos.")
    else:
        form = ProductoForm()

    return render(request, 'agregar_producto.html', {'form': form})


    
@user_passes_test(es_superusuario)
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'admin_productos.html', {'productos': productos})

@user_passes_test(es_superusuario)
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        print("✅ Se recibió un POST para editar el producto.")  
        form = ProductoForm(request.POST, request.FILES, instance=producto)

        if form.is_valid():
            print("✅ El formulario es válido. Guardando cambios.")  
            form.save()
            messages.success(request, "✅ Producto actualizado correctamente.")
            return redirect('/productos/')  # 🔹 Redirigir manualmente a la lista de productos
        else:
            print("❌ Error en el formulario. No se guardaron los cambios.")  
            print("🔴 Errores del formulario:", form.errors)  # 🔥 Mostrar errores en consola
            messages.error(request, "❌ Error al actualizar el producto. Verifica los datos ingresados.")

    else:
        print("📌 Se accedió a la página de edición de producto.")  
        form = ProductoForm(instance=producto)

    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})

@user_passes_test(es_superusuario)
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    messages.success(request, "Producto eliminado correctamente.")
    return redirect('lista_productos')


def producto_detalle(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, "producto_detalle.html", {"producto": producto})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now, timedelta
from decimal import Decimal
from .models import Producto

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = request.session.get("carrito", {})

    cantidad_en_carrito = carrito.get(str(producto_id), {}).get("cantidad", 0)
    stock_disponible = producto.stock_disponible()

    if cantidad_en_carrito >= stock_disponible:
        messages.error(request, f"Solo puedes añadir {stock_disponible} unidades de {producto.nombre}.")
    else:
        if str(producto_id) in carrito:
            carrito[str(producto_id)]["cantidad"] += 1
        else:
            carrito[str(producto_id)] = {
                "nombre": producto.nombre,
                "precio": str(producto.precio),
                "cantidad": 1,
                "agregado_hora": str(now()),
            }

        # ✅ Asegurar que `stock_reservado` no supere `stock`
        if producto.stock_reservado < producto.stock:
            producto.stock_reservado += 1
            producto.stock -= 1  # **Restar del stock real**
            producto.save()

        request.session["carrito"] = carrito
        messages.success(request, f"Se añadió {producto.nombre} al carrito.")

    return redirect("producto_detalle", producto_id=producto_id)

def carrito(request):
    carrito = request.session.get("carrito", {})
    productos = []
    total = Decimal(0)
    tiempo_actual = now()

    for producto_id, datos in list(carrito.items()):
        producto = Producto.objects.get(id=int(producto_id))
        agregado_hora = datos.get("agregado_hora", None)

        # 🔹 Si han pasado más de 10 minutos, liberar stock
        if agregado_hora and now() - timedelta(minutes=10) > tiempo_actual:
            print(f"⏳ Expirando reserva de {producto.nombre}. Liberando {datos['cantidad']} unidades.")

            producto.stock_reservado -= datos["cantidad"]
            producto.stock += datos["cantidad"]  # ✅ Devolver stock real
            if producto.stock_reservado < 0:
                producto.stock_reservado = 0
            producto.save()
            del carrito[producto_id]  # **Elimina el producto del carrito**
        else:
            cantidad_real = datos["cantidad"]
            subtotal = Decimal(producto.precio) * cantidad_real
            productos.append({'producto': producto, 'cantidad': cantidad_real, 'subtotal': subtotal})
            total += subtotal

    request.session["carrito"] = carrito  # Guardar el carrito actualizado

    return render(request, 'carrito.html', {
        'productos': productos,
        'total': total,
    })



def reducir_cantidad_carrito(request, producto_id):
    carrito = request.session.get("carrito", {})

    if str(producto_id) in carrito:
        producto = Producto.objects.get(id=producto_id)

        if carrito[str(producto_id)]["cantidad"] > 1:
            carrito[str(producto_id)]["cantidad"] -= 1
            producto.stock_reservado -= 1
            producto.stock += 1  # ✅ **Devolver stock real**
        else:
            producto.stock_reservado -= 1
            producto.stock += 1  # ✅ **Devolver stock real**
            del carrito[str(producto_id)]

        # ✅ Evitar valores negativos
        if producto.stock_reservado < 0:
            producto.stock_reservado = 0

        producto.save()

    request.session["carrito"] = carrito
    messages.success(request, "Cantidad actualizada correctamente.")

    return redirect("carrito")




def vaciar_carrito(request):
    carrito = request.session.get("carrito", {})

    for producto_id, datos in carrito.items():
        producto = Producto.objects.get(id=int(producto_id))

        # ✅ Asegurar que `stock_reservado` se libere completamente
        producto.stock_reservado -= datos["cantidad"]
        producto.stock += datos["cantidad"]  # ✅ Devolver stock real

        # ✅ Evitar valores negativos
        if producto.stock_reservado < 0:
            producto.stock_reservado = 0

        producto.save()

    request.session["carrito"] = {}  # Vaciar el carrito
    messages.success(request, "Carrito vaciado correctamente.")

    return redirect("carrito")



def checkout(request):
    return render(request, "checkout.html")  # Asegúrate de tener "checkout.html" en templates/
