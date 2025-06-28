"""
RUTAS DE ADMIN DE LA API CUENTAS
"""

from ..utils.permissions import PermisoAdmin, PermisoFuncionario
from ..models import Usuario
from ..serializers.admin import (
    UsuarioAdminListSerializer,
    UsuarioCreateAdminSerializer,
    UsuarioAdminUpdateSerializer
)
from rest_framework.response import Response
from rest_framework import status, generics
from django.db import IntegrityError
from ..utils.paginations import CuentasAdminPagination


#* RUTAS PARA CREAR Y LISTAR USUARIOS (ADMIN)
#24/06/25

class UsuarioAdminListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [PermisoAdmin]
    pagination_class = CuentasAdminPagination

    #método queryset personalizado para excluir superusuarios
    #28/06/25
    def get_queryset(self):
        return Usuario.objects.filter(is_superuser=False).order_by('username')

    #método para definir el serializer según método HTTP
    #28/06/25
    def get_serializer_class(self):
        #si es GET, define serializer UsuarioAdminListSerializer
        if self.request.method == 'GET':
            return UsuarioAdminListSerializer
        #si es POST, define serializer UsuarioCreateAdminSerializer
        return UsuarioCreateAdminSerializer

    #método create (POST)
    #28/06/25
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            try:
                usuario = serializer.save()
            except IntegrityError:
                return Response({
                    "status": "error",
                    "message": "Hubo un error al crear el usuario",
                    "errors": {"telefono": ["El teléfono ya existe o es inválido."]}
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "status": "success",
                "message": f"Usuario {usuario.get_username()} creado correctamente",
                "usuario": {
                    "username": usuario.get_username(),
                    "rol": usuario.get_rol_display()
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "message": "Hubo un error al crear el usuario",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

###############################################################################################

#* RUTA PARA FILTRAR USUARIO POR USERNAME Y ACTUALIZAR DATOS
#28/06/25

class UsuarioAdminRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Usuario.objects.all()
    permission_classes = [PermisoFuncionario]
    lookup_field = 'username' #campo de filtro

    #método para identificar serializer según método HTTP
    #28/06/25
    def get_serializer_class(self):
        #si es GET, usa serializer UsuarioAdminListSerializer
        if self.request.method == 'GET':
            return UsuarioAdminListSerializer
        #si es PUT/PATCH, usa serializer UsuarioAdminUpdateSerializer
        return UsuarioAdminUpdateSerializer

    #método patch
    #28/06/25
    def patch(self, request, *args, **kwargs):
        usuario = self.get_object()
        serializer = self.get_serializer(usuario, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Usuario actualizado correctamente",
                "usuario": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "message": "No se pudo actualizar el usuario",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    #método put
    #28/06/25
    def put(self, request, *args, **kwargs):
        usuario = self.get_object()
        serializer = self.get_serializer(usuario, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Usuario actualizado correctamente",
                "usuario": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "message": "No se pudo actualizar el usuario",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)