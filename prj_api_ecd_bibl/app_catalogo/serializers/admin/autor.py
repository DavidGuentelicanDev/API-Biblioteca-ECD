"""
SERIALIZERS DE AUTOR
"""

from rest_framework import serializers
from ...models import Autor


#* SERIALIZER PARA AUTOR, INCLUYE TODOS LOS MÉTODOS NECESARIOS
#25/06/25

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ['id', 'nombre', 'pseudonimo']