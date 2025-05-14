from rest_framework import serializers
from .models import RepartidorLocation

class RepartidorLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepartidorLocation
        fields = ('id', 'repartidor', 'latitude', 'longitude', 'timestamp')
