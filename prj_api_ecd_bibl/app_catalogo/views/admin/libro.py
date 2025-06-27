"""
RUTAS DE EDITORIAL
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from ...models import Libro
from ...serializers.admin.libro import LibroCreateSerializer, LibroListSerializer
from django.db import IntegrityError


#* RUTA PARA LISTAR Y CREAR LIBROS
#26/06/25

class LibroListCreateAPIView(generics.ListCreateAPIView):
    queryset = Libro.objects.all()
    permission_classes = [AllowAny]

    #método para identificar serializer según método GET o POST
    #26/06/25
    def get_serializer_class(self):
        #si es POST, usa serializer LibroCreateSerializer
        if self.request.method == 'POST':
            return LibroCreateSerializer
        #si es GET, usa serializer LibroListSerializer
        return LibroListSerializer

    #método create para crear libro
    #26/06/25
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            try:
                libro = serializer.save()
            except IntegrityError:
                return Response({
                    "status": "error",
                    "message": "No se puede asociar el mismo autor más de una vez al libro.",
                    "errors": {"autores": ["No repitas autores en la lista."]}
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "status": "success",
                "message": f"Libro '{str(libro)}' creado exitosamente.",
                "libro": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "message": "No se pudo crear el libro.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)