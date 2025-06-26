"""
RUTAS DE EDITORIAL
"""

from rest_framework.response import Response
from rest_framework import generics, status
from ...models import Autor
from ...serializers.admin.autor import AutorSerializer
from rest_framework.permissions import AllowAny


#* RUTA PARA LISTAR TODOS LOS AUTORES / CREAR AUTORES
#25/06/25

class AutorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    permission_classes = [AllowAny]

    #método para ruta post (create)
    #25/06/25
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            autor = serializer.save()
            return Response({
                "status": "success",
                "message": f"Autor {str(autor)} creado exitosamente.",
                "autor": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "message": "Error al crear el autor.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)