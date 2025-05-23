# Generated by Django 5.1.6 on 2025-03-30 06:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "mi_proyecto",
            "0014_pedido_es_suscripcion_pedido_estado_suscripcion_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Mascota",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=100)),
                (
                    "especie",
                    models.CharField(
                        choices=[
                            ("perro", "Perro"),
                            ("gato", "Gato"),
                            ("otro", "Otro"),
                        ],
                        max_length=20,
                    ),
                ),
                ("raza", models.CharField(blank=True, max_length=100, null=True)),
                ("fecha_nacimiento", models.DateField(blank=True, null=True)),
                (
                    "foto",
                    models.ImageField(blank=True, null=True, upload_to="mascotas/"),
                ),
                (
                    "propietario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mascotas",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
