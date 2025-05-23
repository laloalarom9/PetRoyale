# Generated by Django 5.1.6 on 2025-03-30 07:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mi_proyecto", "0016_pedido_mascota"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pedido",
            name="mascota",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="pedidos_asociados",
                to="mi_proyecto.mascota",
            ),
        ),
    ]
