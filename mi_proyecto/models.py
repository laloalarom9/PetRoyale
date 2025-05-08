import logging
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.db import models
from django.contrib.auth import get_user_model
from django.apps import apps
from django.conf import settings


class CustomUser(AbstractUser):
    GENERO_CHOICES = [
        ("hombre", "Hombre"),
        ("mujer", "Mujer"),
    ]

    apellido2 = models.CharField(max_length=50, blank=True, null=True)  # Segundo apellido opcional
    num_tel = models.CharField(max_length=15, blank=True, null=True)  # Número de teléfono
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES, default="hombre")  # Nuevo campo de género
    direccion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

    # Relación con grupos y permisos para evitar errores en Django Admin
    groups = models.ManyToManyField(Group, related_name="customuser_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions")

    def save(self, *args, **kwargs):
        logging.info(f"User {self.username} saved")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        logging.info(f"User {self.username} deleted")
        super().delete(*args, **kwargs)#




class Producto(models.Model):
    CATEGORIAS = [
        ("perros", "Perros"),
        ("gatos", "Gatos"),
        ("otros", "Otros"),
    ]

    EDAD_CHOICES = [
        ("cachorro", "Cachorro"),
        ("adulto", "Adulto"),
        ("senior", "Senior"),
    ]

    TAMANOS = [
        ("pequeño", "Pequeño"),
        ("mediano", "Mediano"),
        ("grande", "Grande"),
    ]

    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)  # Stock real
    stock_reservado = models.PositiveIntegerField(default=0)  # 🔹 Nuevo campo para stock reservado en carritos
    imagen = models.ImageField(upload_to="productos/", null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # 🔹 Nuevos campos para filtros
    categoria = models.CharField(max_length=10, choices=CATEGORIAS, default="otros")
    marca = models.CharField(max_length=50, blank=True, null=True)
    edad_recomendada = models.CharField(max_length=10, choices=EDAD_CHOICES, blank=True, null=True)
    tamano_mascota = models.CharField(max_length=10, choices=TAMANOS, blank=True, null=True)
    
    def stock_disponible(self):
        """
        Calcula y devuelve el stock real disponible para la compra.
        Se asegura de que no haya inconsistencias en stock y stock_reservado.
        """

        cambios_realizados = False  # 🔹 Para saber si necesitamos guardar los cambios

        # 🔹 Asegurar que los valores nunca sean negativos
        if self.stock < 0:
            print(f"⚠️ ERROR en {self.nombre}: Stock NEGATIVO detectado ({self.stock}). Ajustando a 0.")
            self.stock = 0
            cambios_realizados = True  # ✅ Hay un cambio que debemos guardar

        if self.stock_reservado < 0:
            print(f"⚠️ ERROR en {self.nombre}: Stock reservado NEGATIVO detectado ({self.stock_reservado}). Ajustando a 0.")
            self.stock_reservado = 0
            cambios_realizados = True  # ✅ Hay un cambio que debemos guardar

        # 🔹 Si el stock reservado es mayor que el stock total, corregimos el error
        if self.stock_reservado > self.stock:
            print(f"⚠️ ERROR en {self.nombre}: Stock reservado ({self.stock_reservado}) es mayor que stock real ({self.stock}). Ajustando valores.")
            self.stock_reservado = self.stock
            cambios_realizados = True  # ✅ Hay un cambio que debemos guardar

        # 🔹 Calcular stock disponible correctamente
        disponible = self.stock - self.stock_reservado

        # 🔹 Si por algún motivo el stock disponible es negativo, ajustarlo a 0
        if disponible < 0:
            disponible = 0

        # 🔹 Guardar cambios si hubo ajustes
        if cambios_realizados:
            self.save()

        print(f"✅ STOCK - {self.nombre}: Stock={self.stock}, Reservado={self.stock_reservado}, Disponible={disponible}")
        return disponible

    def __str__(self):
        return f"{self.nombre} ({self.categoria})"#




User = get_user_model()
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now
import uuid
import requests

class Pedido(models.Model):
    ESTADOS_PEDIDO = [
        ("pendiente", "Pendiente"),
        ("procesando", "En proceso"),
        ("enviado", "Enviado"),
        ("entregado", "Entregado"),
    ]

    ESTADOS_SUSCRIPCION = [
        ("activa", "Activa"),
        ("pendiente_cancelacion", "Pendiente de cancelación"),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pedidos")
    numero_pedido = models.CharField(max_length=30, unique=True)
    fecha_pedido = models.DateTimeField(default=now)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total_con_iva = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=30, choices=ESTADOS_PEDIDO, default="pendiente")

    es_suscripcion = models.BooleanField(default=False)
    estado_suscripcion = models.CharField(max_length=30, choices=ESTADOS_SUSCRIPCION, default="activa")
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    # 👇 NUEVO: mascota vinculada a la suscripción
    mascota = models.ForeignKey(
        "Mascota",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="suscripciones"
    )
    def __str__(self):
        return f"Pedido {self.numero_pedido} - {self.usuario.username}"
    
    def save(self, *args, **kwargs):
        # Si no tenemos lat/lng pero sí dirección
        if (not self.lat or not self.lng) and self.usuario.direccion:
            direccion = self.usuario.direccion
            api_key = settings.GOOGLE_MAPS_API_KEY  # Usa la API Key de settings.py
            url = f"https://maps.googleapis.com/maps/api/geocode/json?address={direccion.replace(' ', '+')}&key={api_key}"
            
            response = requests.get(url)
            data = response.json()

            if data['status'] == 'OK':
                location = data['results'][0]['geometry']['location']
                self.lat = location['lat']
                self.lng = location['lng']
            else:
                print(f"⚠️ No se pudo geocodificar la dirección: {direccion}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido {self.numero_pedido} - {self.usuario.username}"
    
class DetallePedido(models.Model):
    pedido = models.ForeignKey("Pedido", on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey("Producto", on_delete=models.CASCADE)  # ✅ Se pasa como string para evitar el ciclo
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Pedido {self.pedido.id}"

class Reseña(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="reseñas")
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Opcional
    nombre = models.CharField(max_length=100, blank=True, help_text="Tu nombre (opcional)")
    contenido = models.TextField(verbose_name="Reseña")
    valoracion = models.PositiveSmallIntegerField(default=5,validators=[MinValueValidator(1), MaxValueValidator(5)])  # 1 a 5 estrellas por ejemplo
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reseña para {self.producto.nombre} - {self.valoracion}★"



class Mascota(models.Model):
    ESPECIES = [
        ("perro", "Perro"),
        ("gato", "Gato"),
        ("otro", "Otro"),
    ]

    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=20, choices=ESPECIES)
    raza = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    foto = models.ImageField(upload_to="mascotas/", blank=True, null=True)  # Nueva imagen opcional
    propietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mascotas")

    def get_foto_url(self):
        if self.foto:
            return self.foto.url
        if self.especie == "perro":
            return "/static/img/defaults/perro.png"
        elif self.especie == "gato":
            return "/static/img/defaults/gato.png"
        else:
            return "/static/img/defaults/otro.png"

    def __str__(self):
        return f"{self.nombre} ({self.especie})"


from django.utils import timezone

class Repartidor(models.Model): 
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="repartidor_profile") 
    sueldo = models.FloatField()
    def __str__(self):
        return self.user.username
    
class RepartidorLocation(models.Model): 
    repartidor = models.ForeignKey(Repartidor, on_delete=models.CASCADE, related_name="locations") 
    latitude = models.DecimalField(max_digits=9, decimal_places=6) 
    longitude = models.DecimalField(max_digits=9, decimal_places=6) 
    timestamp = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.repartidor.user.username}: {self.latitude}, {self.longitude} at {self.timestamp}"

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()

class Ruta(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    repartidor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rutas')
    fecha = models.DateTimeField(default=now)
    pedidos = models.ManyToManyField('Pedido', related_name='rutas', blank=True)

    def __str__(self):
        return f"Ruta: {self.nombre} - Repartidor: {self.repartidor.username}"


# models.py
from django.db import models

class Refugio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre