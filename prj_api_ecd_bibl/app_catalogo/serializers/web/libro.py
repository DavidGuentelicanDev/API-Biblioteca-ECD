"""
SERIALIZERS DE LIBRO ADMIN
"""

from rest_framework import serializers
from ...models import Libro, Autor, AutorPorLibro
from .autor import AutorSerializer
from .editorial import EditorialSerializer


#* SERIALIZER PARA LISTAR LIBROS WEB
#28/06/25

class LibroWebListSerializer(serializers.ModelSerializer):
    autores = serializers.SerializerMethodField()
    categoria_nombre = serializers.CharField(source='get_categoria_display', read_only=True)
    portada_url = serializers.SerializerMethodField()

    class Meta:
        model = Libro
        fields = [
            'codigo',
            'titulo',
            'autores',
            'categoria_nombre',
            'portada_url'
        ]

    #llama al método str del modelo autor por autor
    #28/06/25
    def get_autores(self, obj):
        autores = Autor.objects.filter(autorporlibro__libro=obj)
        return [str(autor) for autor in autores]

    #llama al método que obtiene la url de la portada en string
    #28/06/25
    def get_portada_url(self, obj):
        return obj.get_portada()