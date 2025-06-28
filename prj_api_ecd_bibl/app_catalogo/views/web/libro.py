"""
RUTAS DE LIBRO WEB
"""

from rest_framework import generics, status
from rest_framework.response import Response
from ...models import Libro
from ...serializers.web.libro import LibroWebListSerializer, LibroWebRetrieveSerializer
from rest_framework.permissions import AllowAny


#* RUTA PARA LISTAR TODOS LOS LIBROS
#28/06/25

class LibroListAPIView(generics.ListAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroWebListSerializer
    permission_classes = [AllowAny]

#############################################################################################

#* RUTA PARA OBTENER LIBRO POR CÓDIGO
#28/06/25

class LibroRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroWebRetrieveSerializer
    permission_classes = [AllowAny]
    lookup_field = 'codigo' #código en vez de id