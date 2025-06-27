"""
SERIALIZERS DE LIBRO
"""

from rest_framework import serializers
from ...models import Libro, Autor, AutorPorLibro


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

    #método create
    #26/06/25
    def create(self, validated_data):
        autores = validated_data.pop('autores')
        libro = Libro.objects.create(**validated_data)

        for autor in autores:
            AutorPorLibro.objects.create(codigo_libro=libro, id_autor=autor)

        return libro