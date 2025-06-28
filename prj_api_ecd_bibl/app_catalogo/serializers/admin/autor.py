"""
SERIALIZERS DE AUTOR ADMIN
"""

from rest_framework import serializers
from ...models import Autor


#* SERIALIZER PARA AUTOR ADMIN
#25/06/25

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ['id', 'nombre', 'pseudonimo']