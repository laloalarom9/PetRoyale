# Generated by Django 5.1.6 on 2025-04-26 19:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mi_proyecto", "0019_repartidor_repartidorlocation_ruta"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="direccion",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
