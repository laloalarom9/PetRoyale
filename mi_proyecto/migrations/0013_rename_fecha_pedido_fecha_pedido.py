# Generated by Django 5.1.6 on 2025-03-16 19:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("mi_proyecto", "0012_alter_pedido_estado"),
    ]

    operations = [
        migrations.RenameField(
            model_name="pedido",
            old_name="fecha",
            new_name="fecha_pedido",
        ),
    ]
