"""
SERIALIZERS DE EDITORIAL ADMIN
"""

from rest_framework import serializers
from ...models import Editorial


#* SERIALIZER PARA EDITORIAL ADMIN
#25/06/25

class EditorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editorial
        fields = ['id', 'nombre']