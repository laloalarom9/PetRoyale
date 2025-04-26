import requests
from django.conf import settings

def geocodificar_pedido(pedido):
    """
    Geocodifica un pedido sólo si no tiene latitud/longitud.
    """
    if pedido.lat and pedido.lng:
        print(f"✅ Pedido {pedido.id} ya tiene coordenadas. No se geocodifica.")
        return pedido.lat, pedido.lng  # No hace falta nada

    direccion = pedido.usuario.direccion
    if not direccion:
        print(f"⚠️ El pedido {pedido.id} no tiene dirección asociada.")
        return None, None

    direccion_completa = f"{direccion}, Madrid, España"  # Puedes mejorar esto luego dinámicamente

    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={direccion_completa.replace(' ', '+')}&key={settings.GOOGLE_MAPS_API_KEY}"

    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        pedido.lat = location['lat']
        pedido.lng = location['lng']
        pedido.save()
        print(f"📍 Pedido {pedido.id} actualizado: lat={pedido.lat}, lng={pedido.lng}")
        return pedido.lat, pedido.lng
    else:
        print(f"⚠️ Error geocodificando pedido {pedido.id}: {data.get('error_message', 'Sin mensaje de error')}")
        return None, None
