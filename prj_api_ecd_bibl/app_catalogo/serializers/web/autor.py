"""
SERIALIZERS DE AUTOR WEB
"""

from rest_framework import serializers
from ...models import Autor


#* SERIALIZER PARA AUTOR WEB
#28/06/25

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ['nombre', 'pseudonimo']