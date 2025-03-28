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

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pedido, DetallePedido


def pedidos(request):
    if not request.user.is_authenticated:
        return render(request, "requiere_login.html")
    """
    Vista para mostrar los pedidos del usuario autenticado con los detalles de productos comprados.
    """
    pedidos = Pedido.objects.filter(usuario=request.user).order_by("-fecha_pedido")  # ✅ CORREGIDO
    pedidos_con_detalles = []

    for pedido in pedidos:
        detalles = DetallePedido.objects.filter(pedido=pedido)
        pedidos_con_detalles.append({"pedido": pedido, "detalles": detalles})

    return render(request, "pedidos.html", {"pedidos_con_detalles": pedidos_con_detalles})

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
    stock_disponible = producto.stock_disponible()  # ✅ Llama al método correctamente

    return render(request, "producto_detalle.html", {
        "producto": producto,
        "stock_disponible": stock_disponible,  # ✅ Pásalo como variable al template
    })

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = request.session.get("carrito", {})

    # Obtener la cantidad deseada del formulario
    cantidad = int(request.POST.get("cantidad", 1))

    stock_disponible = producto.stock_disponible()

    if cantidad > stock_disponible:
        messages.error(request, f"Solo puedes añadir {stock_disponible} unidades de {producto.nombre}.")
    else:
        if str(producto_id) in carrito:
            carrito[str(producto_id)]["cantidad"] += cantidad
        else:
            carrito[str(producto_id)] = {
                "nombre": producto.nombre,
                "precio": str(producto.precio),
                "cantidad": cantidad,  # ✅ Ahora se suma correctamente la cantidad
                "agregado_hora": str(now()),
            }

        # ✅ SOLO aumentar el stock reservado
        if producto.stock_reservado + cantidad <= producto.stock:
            producto.stock_reservado += cantidad
            producto.save()  # Guardar cambios

        request.session["carrito"] = carrito
        messages.success(request, f"Se añadieron {cantidad} unidades de {producto.nombre} al carrito.")

    return redirect("producto_detalle", producto_id=producto_id)




from decimal import Decimal, ROUND_HALF_UP

from decimal import Decimal, ROUND_HALF_UP

from decimal import Decimal, ROUND_HALF_UP

def carrito(request):
    carrito = request.session.get("carrito", {})
    productos = []
    total = Decimal(0)

    
    for key, datos in carrito.items():
        if isinstance(datos, dict) and datos.get("tipo") == "suscripcion":
            try:
                producto = Producto.objects.get(id=datos["producto_id"])
                duracion = int(datos["duracion"])
                subtotal = Decimal(producto.precio) * duracion

                productos.append({
                    "clave": key,  # Necesario para el botón
                    "producto": producto,  # ← Pasamos el objeto real
                    "tipo": "suscripcion",  # ← Para detectar en el template
                    "precio": producto.precio,
                    "cantidad": f"{duracion} mes(es)",
                    "subtotal": subtotal
                })

                total += subtotal
            except (KeyError, Producto.DoesNotExist):
                continue  # Silenciosamente ignorar si falla

        elif key.isdigit():
            producto = Producto.objects.get(id=int(key))
            cantidad = datos["cantidad"]
            subtotal = Decimal(producto.precio) * cantidad

            productos.append({
                "producto": producto,  # ← También aquí
                "tipo": "compra",      # ← Para que sea consistente
                "precio": producto.precio,
                "cantidad": cantidad,
                "subtotal": subtotal
            })

            total += subtotal

    # Calcular IVA y total
    iva = (total * Decimal(0.21)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    total_con_iva = (total + iva).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    return render(request, 'carrito.html', {
        'productos': productos,
        'total': total,
        'iva': iva,
        'total_con_iva': total_con_iva,
    })


def reducir_cantidad_carrito(request, producto_id):
    carrito = request.session.get("carrito", {})

    if str(producto_id) in carrito:
        producto = Producto.objects.get(id=producto_id)
        cantidad_actual = carrito[str(producto_id)]["cantidad"]

        if cantidad_actual > 1:
            carrito[str(producto_id)]["cantidad"] -= 1
            producto.stock_reservado -= 1  # ✅ Devolver solo 1 unidad reservada
        else:
            producto.stock_reservado -= cantidad_actual  # ✅ Devolver toda la cantidad reservada
            del carrito[str(producto_id)]  # Eliminar del carrito solo después de ajustar stock

        # ✅ Asegurar que `stock_reservado` no sea negativo
        producto.stock_reservado = max(producto.stock_reservado, 0)
        producto.save()

    request.session["carrito"] = carrito
    messages.success(request, "Cantidad actualizada correctamente.")

    return redirect("carrito")

def reducir_suscripcion_carrito(request, producto_id):
    carrito = request.session.get("carrito", {})

    # Buscamos una clave que empiece por "suscripcion-" y termine en el ID del producto
    for clave in list(carrito.keys()):
        if clave.startswith("suscripcion-") and clave.endswith(str(producto_id)):
            try:
                del carrito[clave]
                messages.info(request, "Suscripción eliminada del carrito.")
            except KeyError:
                messages.error(request, "No se pudo eliminar la suscripción.")
            break  # Ya encontramos y eliminamos, no seguimos buscando

    request.session["carrito"] = carrito
    return redirect("carrito")





from decimal import Decimal, ROUND_HALF_UP

def calcular_totales(carrito):
    total = Decimal(0)

    for producto_id, datos in carrito.items():
        producto = Producto.objects.get(id=int(producto_id))
        cantidad = datos["cantidad"]
        subtotal = Decimal(producto.precio) * cantidad
        total += subtotal

    # ✅ Redondeo correcto del IVA y total con IVA
    iva = (total * Decimal(0.21)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    total_con_iva = (total + iva).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return total, iva, total_con_iva



def vaciar_carrito(request):
    carrito = request.session.get("carrito", {})

    for producto_id, datos in carrito.items():
        if not str(producto_id).isdigit():
            continue  # Ignorar claves como 'tipo' o 'suscripcion-32-6'
        try:
            producto = Producto.objects.get(id=int(producto_id))

            # ✅ Solo devolver lo que realmente estaba reservado
            producto.stock_reservado -= datos["cantidad"]
            producto.stock_reservado = max(producto.stock_reservado, 0)  # ✅ Evita valores negativos
            producto.save()
        except Producto.DoesNotExist:
            continue  # Por si el producto fue eliminado

    request.session["carrito"] = {}  # Vaciar el carrito en sesión
    messages.success(request, "Carrito vaciado correctamente.")

    return redirect("carrito")


from django.shortcuts import render
from django.utils.timezone import now
from decimal import Decimal

from decimal import Decimal, ROUND_HALF_UP




def checkout(request):
    carrito = request.session.get("carrito", {})
    productos = []
    total = Decimal(0)

    for key, datos in carrito.items():
        if isinstance(datos, dict) and datos.get("tipo") == "suscripcion":
            try:
                producto = Producto.objects.get(id=datos["producto_id"])
                duracion = int(datos["duracion"])
                subtotal = Decimal(producto.precio) * duracion

                productos.append({
                    "producto": producto,  # ← Pasamos el objeto real
                    "tipo": "suscripcion",  # ← Para detectar en el template
                    "precio": producto.precio,
                    "cantidad": f"{duracion} mes(es)",
                    "subtotal": subtotal
                })

                total += subtotal
            except (KeyError, Producto.DoesNotExist):
                continue  # Silenciosamente ignorar si falla

        elif key.isdigit():
            producto = Producto.objects.get(id=int(key))
            cantidad = datos["cantidad"]
            subtotal = Decimal(producto.precio) * cantidad

            productos.append({
                "producto": producto,  # ← También aquí
                "tipo": "compra",      # ← Para que sea consistente
                "precio": producto.precio,
                "cantidad": cantidad,
                "subtotal": subtotal
            })

            total += subtotal

    # Totales
    iva = (total * Decimal("0.21")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    total_con_iva = (total + iva).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return render(request, "checkout.html", {
        "productos": productos,
        "total": total,
        "iva": iva,
        "total_con_iva": total_con_iva
    })



    
import io
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.contrib import messages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from decimal import Decimal
from .models import Producto

from .models import Pedido, DetallePedido
import io
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.contrib import messages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from decimal import Decimal, ROUND_HALF_UP
from .models import Pedido, DetallePedido, Producto


def procesar_compra(request):
    carrito = request.session.get("carrito", {})

    if not carrito:
        messages.error(request, "Tu carrito está vacío.")
        return redirect("carrito")
    #Si es suscripcion
    if carrito.get("tipo") == "suscripcion":
        try:
            producto = Producto.objects.get(id=carrito["producto_id"])
            duracion = int(carrito["duracion"])
            total = Decimal(producto.precio) * duracion
            iva = (total * Decimal("0.21")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            total_con_iva = (total + iva).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            pedido = Pedido.objects.create(
                usuario=request.user,
                numero_pedido=f"SUS-{now().strftime('%Y%m%d%H%M%S')}",
                fecha_pedido=now(),
                total=total,
                iva=iva,
                total_con_iva=total_con_iva,
                estado="pendiente"
            )

            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=duracion,
                precio_unitario=producto.precio
            )

            request.session["carrito"] = {}
            return render(request, "confirmacion_compra.html", {
                "numero_pedido": pedido.numero_pedido,
                "total_con_iva": total_con_iva
            })

        except Producto.DoesNotExist:
            messages.error(request, "Producto no encontrado para la suscripción.")
            return redirect("carrito")

    
    usuario = request.user
    fecha_compra = now()
    numero_pedido = f"ORD-{fecha_compra.strftime('%Y%m%d%H%M%S')}"
    total = Decimal(0)
    productos_comprados = []

    # ✅ Verificar disponibilidad de stock antes de procesar la compra
    for producto_id, datos in carrito.items():
        try:
            if not str(producto_id).isdigit():
                continue
            producto = Producto.objects.get(id=int(producto_id))
  
            
        except Producto.DoesNotExist:
            messages.error(request, "Uno de los productos en tu carrito ya no está disponible.")
            return redirect("carrito")

        cantidad = datos["cantidad"]

        if producto.stock < cantidad:
            messages.error(request, f"Stock insuficiente para {producto.nombre}. Solo quedan {producto.stock} unidades.")
            return redirect("carrito")

    # ✅ Procesar la compra
    for producto_id, datos in carrito.items():
        if not str(producto_id).isdigit():
                continue
        producto = Producto.objects.get(id=int(producto_id))
        cantidad = datos["cantidad"]
        subtotal = Decimal(producto.precio) * cantidad
        total += subtotal

        productos_comprados.append({
            "id": producto.id,
            "nombre": producto.nombre,
            "cantidad": cantidad,
            "precio": producto.precio,
            "subtotal": subtotal,
        })

        # ✅ Reducir el stock correctamente
        producto.stock_reservado = max(producto.stock_reservado - cantidad, 0)
        producto.stock = max(producto.stock - cantidad, 0)
        producto.save()

    iva = (total * Decimal(0.21)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    total_con_iva = (total + iva).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # ✅ Guardar el pedido en la base de datos
    try:
        pedido = Pedido.objects.create(
            usuario=usuario,
            numero_pedido=numero_pedido,
            fecha_pedido=fecha_compra,  # ✅ CAMBIO AQUÍ
            total=total,
            iva=iva,
            total_con_iva=total_con_iva,
            estado="pendiente"
        )

        # ✅ Guardar los productos comprados en el detalle del pedido
        for item in productos_comprados:
            producto = Producto.objects.get(id=item["id"])
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=item["cantidad"],
                precio_unitario=item["precio"]
            )

    except Exception as e:
        messages.error(request, f"Ocurrió un error al registrar el pedido: {str(e)}")
        return redirect("carrito")

    # 📄 Generar el PDF del recibo
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle("Recibo de Compra - PetRoyale")

    pdf.drawString(100, 750, "PetRoyale - Recibo de Compra")
    pdf.drawString(100, 730, f"Cliente: {usuario.username} ({usuario.email})")
    pdf.drawString(100, 710, f"Fecha: {fecha_compra.strftime('%d/%m/%Y %H:%M:%S')}")
    pdf.drawString(100, 690, f"Número de pedido: {numero_pedido}")

    y = 650
    pdf.drawString(100, y, "Detalle del pedido:")
    y -= 20
    pdf.drawString(100, y, "--------------------------------------------")

    for item in productos_comprados:
        y -= 20
        pdf.drawString(100, y, f"{item['nombre']} x {item['cantidad']} - {item['precio']:.2f}€ c/u")

    y -= 30
    pdf.drawString(100, y, f"Subtotal: {total:.2f}€")
    y -= 20
    pdf.drawString(100, y, f"IVA (21%): {iva:.2f}€")
    y -= 20
    pdf.drawString(100, y, f"Total con IVA: {total_con_iva:.2f}€")

    pdf.save()
    buffer.seek(0)

    # 📩 Enviar el PDF por correo
    email_subject = "Tu compra en PetRoyale 🛒"
    email_body = render_to_string("email_recibo.html", {
        "usuario": usuario,
        "fecha_compra": fecha_compra.strftime("%d/%m/%Y %H:%M:%S"),
        "numero_pedido": numero_pedido,
        "productos_comprados": productos_comprados,
        "total": f"{total:.2f}",
        "iva": f"{iva:.2f}",
        "total_con_iva": f"{total_con_iva:.2f}",
    })

    email = EmailMessage(
        email_subject,
        email_body,
        "noreply@petroyale.com",
        [usuario.email],
    )
    email.attach("recibo_petroyale.pdf", buffer.getvalue(), "application/pdf")
    email.content_subtype = "html"
    email.send()

    # 🛒 Vaciar el carrito después de la compra
    request.session["carrito"] = {}
    messages.success(request, "Compra realizada con éxito. Recibirás un correo con el recibo.")

    # ✅ Redirigir correctamente a la confirmación de compra
    return render(request, "confirmacion_compra.html", {
        "numero_pedido": numero_pedido,
        "total_con_iva": f"{total_con_iva:.2f}",
    })


from django.contrib.auth.decorators import login_required
from .models import Producto, Reseña  
from .forms import ReseñaForm  


def crear_reseña(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == "POST":
        form = ReseñaForm(request.POST)
        if form.is_valid():
            reseña = form.save(commit=False)
            reseña.producto = producto
            if request.user.is_authenticated:
                reseña.usuario = request.user         
            reseña.save()
            messages.success(request, "¡Tu reseña ha sido guardada!")
            return redirect('producto_detalle', producto_id=producto.id)
    else:
        form = ReseñaForm()

    return render(request, 'crear_reseña.html', {'form': form, 'producto': producto})

from .forms import SuscripcionForm
from django.shortcuts import redirect, get_object_or_404
from .models import Producto

@login_required
def suscribirse(request):
    if request.method == 'POST':
        form = SuscripcionForm(request.POST)
        if form.is_valid():
            suscripcion = form.save(commit=False)
            suscripcion.usuario = request.user
            suscripcion.save()
            return redirect('inicio')
    else:
        form = SuscripcionForm()

    return render(request, 'suscripciones.html', {'form': form})

def suscripciones(request):
    productos = Producto.objects.all()
    return render(request, "suscripciones.html", {"productos": productos})

from django.shortcuts import render, get_object_or_404
from .models import Producto

def seleccionar_suscripcion(request):
    producto_id = request.GET.get("producto_id")
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, "seleccionar_suscripcion.html", {"producto": producto})




def agregar_suscripcion_al_carrito(request):
    if request.method == "POST":
        producto_id = request.POST.get("producto_id")
        duracion = request.POST.get("duracion")

        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            return redirect("suscripciones")

        carrito = request.session.get("carrito", {})

        clave = f"suscripcion-{producto_id}-{duracion}"
        if clave in carrito:
            carrito[clave]["cantidad"] += 1
        else:
            carrito[clave] = {
                "tipo": "suscripcion",
                "producto_id": producto.id,
                "nombre": producto.nombre,
                "precio": float(producto.precio),
                "duracion": duracion,
                "cantidad": 1,
            }

        request.session["carrito"] = carrito
        return redirect("checkout")
