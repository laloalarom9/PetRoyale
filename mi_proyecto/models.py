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
        super().delete(*args, **kwargs)
