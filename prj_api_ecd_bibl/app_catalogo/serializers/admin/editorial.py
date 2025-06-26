"""
SERIALIZERS DE EDITORIAL
"""

from rest_framework import serializers
from ...models import Editorial


#* SERIALIZER PARA EDITORIAL, INCLUYE TODOS LOS METODOS NECESARIOS
#25/06/25

class EditorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editorial
        fields = ['id', 'nombre']