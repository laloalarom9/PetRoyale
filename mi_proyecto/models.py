import logging
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    GENERO_CHOICES = [
        ("hombre", "Hombre"),
        ("mujer", "Mujer"),
    ]

    apellido2 = models.CharField(max_length=50, blank=True, null=True)  # Segundo apellido opcional
    num_tel = models.CharField(max_length=15, blank=True, null=True)  # Número de teléfono
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES, default="hombre")  # Nuevo campo de género

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

        # 🔹 Asegurar que los valores nunca sean negativos
        if self.stock < 0:
            print(f"⚠️ ERROR en {self.nombre}: Stock NEGATIVO detectado ({self.stock}). Ajustando a 0.")
            self.stock = 0

        if self.stock_reservado < 0:
            print(f"⚠️ ERROR en {self.nombre}: Stock reservado NEGATIVO detectado ({self.stock_reservado}). Ajustando a 0.")
            self.stock_reservado = 0

        # 🔹 Si el stock reservado es mayor que el stock total, corregimos el error
        if self.stock_reservado > self.stock:
            print(f"⚠️ ERROR en {self.nombre}: Stock reservado ({self.stock_reservado}) es mayor que stock real ({self.stock}). Ajustando valores.")
            self.stock_reservado = self.stock

        # 🔹 Calcular stock disponible correctamente
        disponible = self.stock - self.stock_reservado

        # 🔹 Si por algún motivo el stock disponible es negativo, ajustarlo a 0
        if disponible < 0:
            disponible = 0

        print(f"✅ STOCK - {self.nombre}: Stock={self.stock}, Reservado={self.stock_reservado}, Disponible={disponible}")
        return disponible


    def __str__(self):
        return f"{self.nombre} ({self.categoria})"
