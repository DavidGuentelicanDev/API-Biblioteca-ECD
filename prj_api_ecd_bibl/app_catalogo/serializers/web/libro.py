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
    categoria = serializers.SerializerMethodField()
    estado = serializers.SerializerMethodField()
    portada_url = serializers.SerializerMethodField()

    class Meta:
        model = Libro
        fields = [
            'codigo',
            'titulo',
            'autores',
            'categoria',
            'estado',
            'portada_url'
        ]

    #llama al método str del modelo autor por autor
    #28/06/25
    def get_autores(self, obj):
        autores = Autor.objects.filter(autorporlibro__libro=obj)
        return [str(autor) for autor in autores]

    #método para listar categoría como objeto
    #28/06/25
    def get_categoria(self, obj):
        return {
            "numero": obj.categoria,
            "nombre": obj.get_categoria_display()
        }

    #método para listar estado como objeto
    #28/06/25
    def get_estado(self, obj):
        return {
            "numero": obj.estado,
            "nombre": obj.get_estado_display()
        }

    #llama al método que obtiene la url de la portada en string
    #28/06/25
    def get_portada_url(self, obj):
        return obj.get_portada()

################################################################################################

#* SERIALIZER PARA MOSTRAR LIBRO POR CODIGO
#28/06/25

class LibroWebRetrieveSerializer(serializers.ModelSerializer):
    titulo_completo = serializers.SerializerMethodField()
    autores = serializers.SerializerMethodField()
    categoria = serializers.SerializerMethodField()
    editorial = serializers.CharField(source='editorial.nombre', read_only=True)
    estado = serializers.SerializerMethodField()
    portada_url = serializers.SerializerMethodField()

    class Meta:
        model = Libro
        fields = [
            'codigo',
            'titulo_completo',
            'autores',
            'resena',
            'categoria',
            'editorial',
            'anio_edicion',
            'estado',
            'portada_url',
        ]

    #llama al método str del modelo libro
    #28/06/25
    def get_titulo_completo(self, obj):
        return str(obj)

    #llama al método str del modelo autor, por autor
    #28/06/25
    def get_autores(self, obj):
        autores = Autor.objects.filter(autorporlibro__libro=obj)
        return [str(autor) for autor in autores]

    #método para listar categoría como objeto
    #28/06/25
    def get_categoria(self, obj):
        return {
            "numero": obj.categoria,
            "nombre": obj.get_categoria_display()
        }

    #método para listar estado como objeto
    #28/06/25
    def get_estado(self, obj):
        return {
            "numero": obj.estado,
            "nombre": obj.get_estado_display()
        }

    #llama al método que obtiene la url de la portada en string
    #28/06/25
    def get_portada_url(self, obj):
        return obj.get_portada()