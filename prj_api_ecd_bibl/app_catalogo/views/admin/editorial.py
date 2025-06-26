"""
RUTAS DE EDITORIAL
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from ...models import Editorial
from ...serializers.admin.editorial import EditorialSerializer
from rest_framework.permissions import AllowAny


#* RUTA PARA LISTAR TODAS LAS EDITORIALES / CREAR EDITORIALES
#25/06/25

class EditorialListCreateAPIView(generics.ListCreateAPIView):
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializer
    permission_classes = [AllowAny]

    #método para ruta post (create)
    #25/06/25
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            editorial = serializer.save()
            return Response({
                "status": "success",
                "message": f"Editorial {str(editorial)} creada exitosamente.",
                "editorial": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Error al crear la editorial.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

############################################################################################

#* RUTA PARA FILTAR EDITORIAL POR ID / EDITAR EDITORIAL POR ID / ELIMINAR EDITORIAL POR ID
#25/06/25

class EditorialRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializer
    permission_classes = [AllowAny]

    #método para ruta put (update)
    #25/06/25
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        nombre = instance.nombre
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            editorial = serializer.save()
            return Response({
                "status": "success",
                "message": f"Editorial {nombre} actualizada exitosamente.",
                "editorial": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": "Error al actualizar la editorial.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    #método para ruta delete
    #25/06/25
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        nombre = instance.nombre
        self.perform_destroy(instance)
        return Response({
            "status": "success",
            "message": f"Editorial {nombre} eliminada exitosamente."
        }, status=status.HTTP_204_NO_CONTENT)