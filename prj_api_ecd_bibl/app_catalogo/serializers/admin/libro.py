"""
SERIALIZERS DE LIBRO
"""

from rest_framework import serializers
from ...models import Libro, Autor, AutorPorLibro
from ...utils.validations import validate_anio_edicion, validate_autores
from django.db import transaction


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
            'categoria',
            'editorial',
            'anio_edicion',
            'portada',
            'autores', #aquí se añadirán los autores en el body json (relación)
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
        # libro = Libro.objects.create(**validated_data)

        # for autor in autores:
        #     AutorPorLibro.objects.create(codigo_libro=libro, id_autor=autor)

        with transaction.atomic():
            libro = Libro.objects.create(**validated_data)

            for autor in autores:
                AutorPorLibro.objects.create(codigo_libro=libro, id_autor=autor)

        return libro