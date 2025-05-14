from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Pedido
from mi_proyecto.utils.geocoding import geocodificar_pedido

@receiver(post_save, sender=Pedido)
def geocodificar_pedido_post_save(sender, instance, created, **kwargs):
    if created:  # Sólo si el pedido es nuevo
        print(f"📦 Pedido {instance.id} creado. Geocodificando...")
        geocodificar_pedido(instance)
