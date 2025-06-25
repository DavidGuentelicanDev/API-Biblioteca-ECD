"""
RUTAS DE ADMIN DE LA API CUENTAS
"""

from rest_framework.views import APIView
from ..utils.permissions import PermisoAdmin, PermisoFuncionario
from ..models import Usuario
from ..serializers.admin import UsuarioAdminListSerializer, UsuarioCreateAdminSerializer, UsuarioAdminUpdateSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from django.db import IntegrityError


#RUTAS PARA CREAR Y LISTAR USUARIOS (ADMIN)
#24/06/25

class UsuarioAdminListCreateAPIView(APIView):
    permission_classes = [PermisoAdmin]

    #RUTA GET PARA OBTENER TODOS LOS USUARIOS
    #24/06/25
    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioAdminListSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #RUTA POST PARA CREAR USUARIOS
    #24/06/25
    def post(self, request):
        serializer = UsuarioCreateAdminSerializer(data=request.data)

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
                    "id": usuario.pk,
                    "username": usuario.get_username(),
                    "rol": usuario.get_rol(),
                    "rol_nombre": usuario.get_rol_display()
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "message": "Hubo un error al crear el usuario",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

###############################################################################################

#RUTA PARA OBTENER USUARIO POR ID (ADMIN)
#22/06/25

class UsuarioAdminRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioAdminListSerializer
    permission_classes = [PermisoFuncionario]

###############################################################################################

#RUTA PARA ACTUALIZAR DATOS DE USUARIO (ADMIN)
#23/06/25

class UsuarioAdminUpdateAPIView(generics.UpdateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioAdminUpdateSerializer
    permission_classes = [PermisoAdmin]

    #metodo patch
    #23/06/25
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