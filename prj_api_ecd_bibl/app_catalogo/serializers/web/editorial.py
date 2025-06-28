"""
SERIALIZERS DE EDITORIAL WEB
"""

from rest_framework import serializers
from ...models import Editorial


#* SERIALIZER PARA EDITORIAL WEB
#28/06/25

class EditorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editorial
        fields = ['nombre']