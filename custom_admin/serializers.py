from rest_framework import serializers
from .models import LicenseKey 


class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenseKey
        fields = ('key', 'created_time', 'is_active')

        