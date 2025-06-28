"""
RUTAS DE LIBRO ADMIN
"""

from rest_framework import generics, status
from rest_framework.response import Response
from ...models import Libro
from ...serializers.admin.libro import LibroCreateSerializer, LibroAdminListSerializer, LibroUpdateSerializer
from django.db import IntegrityError
from app_cuentas.utils.permissions import PermisoBibliotecario, PermisoFuncionario


#* RUTA PARA LISTAR Y CREAR LIBROS
#26/06/25

class LibroListCreateAPIView(generics.ListCreateAPIView):
    queryset = Libro.objects.all()

    #método para identificar permisos según método HTTP
    #28/06/25
    def get_permissions(self):
        #si es GET, permiso de funcionario
        if self.request.method == 'GET':
            return [PermisoFuncionario()]
        #si es POST, permiso de bibliotecario
        return [PermisoBibliotecario()]

    #método para identificar serializer según método GET o POST
    #26/06/25
    def get_serializer_class(self):
        #si es POST, usa serializer LibroCreateSerializer
        if self.request.method == 'POST':
            return LibroCreateSerializer
        #si es GET, usa serializer LibroListSerializer
        return LibroAdminListSerializer

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

##################################################################################################

#* RUTA PARA LISTAR LIBROS POR ID | ACTUALIZAR LIBRO POR ID | ELIMINAR LIBRO POR ID
#28/06/25

class LibroRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Libro.objects.all()
    lookup_field = 'codigo'

    #método para identificar permisos según método HTTP
    #28/06/25
    def get_permissions(self):
        #si es GET, permiso de funcionario
        if self.request.method == 'GET':
            return [PermisoFuncionario()]
        #si es POST, permiso de bibliotecario
        return [PermisoBibliotecario()]

    #método para identificar serializer según método GET o PUT/PATCH
    #28/06/25
    def get_serializer_class(self):
        #si es GET, usa el serializer LibroListSerializer
        if self.request.method == 'GET':
            return LibroAdminListSerializer
        #si es PUT/PATCH, esa el serializer LibroUpdateSerializer
        return LibroUpdateSerializer

    #método update
    #28/06/25
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

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
                "message": f"Libro '{str(libro)}' actualizado exitosamente.",
                "libro": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "message": "No se pudo actualizar el libro.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    #método destroy
    #28/06/25
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        nombre = str(instance)

        try:
            self.perform_destroy(instance)
            return Response({
                "status": "success",
                "message": f"Libro '{nombre}' eliminado exitosamente."
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Error al borrar el libro.",
                "errors": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)