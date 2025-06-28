"""
SERIALIZERS DE LIBRO
"""

from rest_framework import serializers
from ...models import Libro, Autor, AutorPorLibro
from ...utils.validations import validate_anio_edicion, validate_autores
from django.db import transaction
from .autor import AutorSerializer
from .editorial import EditorialSerializer


#* SERIALIZER PARA CREAR LIBRO
#26/06/25

class LibroCreateSerializer(serializers.ModelSerializer):
    #permite añadir autores al libro, mínimo 1
    autores = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Autor.objects.all()),
        min_length=1,
        write_only=True
    )

    class Meta:
        model = Libro
        #sin campo estado
        fields = [
            'codigo',
            'titulo',
            'subtitulo',
            'resena',
            'autores', #aquí se añadirán los autores en el body json (relación)
            'categoria',
            'editorial',
            'anio_edicion',
            'portada',
        ]

    #validación de año edición
    #26/06/25
    def validate_anio_edicion(self, value):
        return validate_anio_edicion(value)

    #validación autores repetidos
    def validate_autores(self, value):
        return validate_autores(value)

    #método create
    #26/06/25
    def create(self, validated_data):
        autores = validated_data.pop('autores')

        #asegura atomicidad el crear en distintas tablas
        with transaction.atomic():
            libro = Libro.objects.create(**validated_data)

            for autor in autores:
                AutorPorLibro.objects.create(codigo_libro=libro, id_autor=autor)

        return libro

#################################################################################################

#* SERIALIZER PARA LISTAR TODOS LOS LIBROS
#26/06/25

class LibroListSerializer(serializers.ModelSerializer):
    autores = serializers.SerializerMethodField() #serializa todos los autores
    editorial = serializers.SerializerMethodField() #serializa la editorial
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True) #permite traer el nombre de la categoría
    estado_display = serializers.CharField(source='get_estado_display', read_only=True) #permite traer el nombre del estado
    portada_url = serializers.SerializerMethodField() #permite traer solo la url de la portada

    class Meta:
        model = Libro
        fields = [
            'codigo',
            'titulo',
            'subtitulo',
            'resena',
            'autores',
            'categoria',
            'categoria_display',
            'editorial',
            'anio_edicion',
            'estado',
            'estado_display',
            'portada_url',
        ]

    #método para obtener los autores de la tabla AutorPorLibro
    #26/06/25
    def get_autores(self, obj):
        autores = Autor.objects.filter(autorporlibro__codigo_libro=obj)
        return AutorSerializer(autores, many=True).data

    #método para obtener la editorial
    #26/06/25
    def get_editorial(self, obj):
        return EditorialSerializer(obj.editorial).data

    #método para obtener la url de la portada
    #26/06/25
    def get_portada_url(self, obj):
        return obj.get_portada()

#################################################################################################

#* SERIALIZER PARA ACTUALIZAR LIBRO
#28/06/25

class LibroUpdateSerializer(serializers.ModelSerializer):
    autores = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Autor.objects.all()),
        min_length=1,
        write_only=True
    )

    class Meta:
        model = Libro
        #incluye estado pero NO incluye código
        fields = [
            'titulo',
            'subtitulo',
            'resena',
            'autores',
            'categoria',
            'editorial',
            'anio_edicion',
            'portada',
            'estado',
        ]

    #validaciones de campos
    #28/06/25

    def validate_anio_edicion(self, value):
        return validate_anio_edicion(value)

    def validate_autores(self, value):
        return validate_autores(value)

    #método update
    #28/06/25
    def update(self, instance, validated_data):
        autores = validated_data.pop('autores', None)

        with transaction.atomic():
            #actualiza los campos de libro
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            if autores is not None:
                #elimina relaciones antiguas y crea nuevas
                AutorPorLibro.objects.filter(codigo_libro=instance).delete()

                for autor in autores:
                    AutorPorLibro.objects.create(codigo_libro=instance, id_autor=autor)

        return instance