from rest_framework import serializers
from .models import Measurement


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('id', 'datetime', 'temperature', 'humidity', 'light', 'is_loud', 'is_valid', 'device_id')
        ordering = ['-id']
