"""
RUTAS DE LIBRO WEB
"""

from rest_framework import generics
from ...models import Libro
from ...serializers.web.libro import LibroWebListSerializer, LibroWebRetrieveSerializer
from rest_framework.permissions import AllowAny
from ...utils.paginations import WebPagination


#* RUTA PARA LISTAR TODOS LOS LIBROS
#28/06/25

class LibroListAPIView(generics.ListAPIView):
    queryset = Libro.objects.all().order_by('codigo')
    serializer_class = LibroWebListSerializer
    permission_classes = [AllowAny]
    pagination_class = WebPagination

#############################################################################################

#* RUTA PARA OBTENER LIBRO POR CÓDIGO
#28/06/25

class LibroRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroWebRetrieveSerializer
    permission_classes = [AllowAny]
    lookup_field = 'codigo' #código en vez de id