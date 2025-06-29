"""
RUTAS GENERALES DE LA API CUENTAS
"""

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics, status
from ..models import Usuario
from ..serializers.general import (
    UsuarioInicialActivarSerializer,
    RecuperarPasswordSerializer,
    ValidarUsernameSerializer
)
from rest_framework.views import APIView
from ..utils.emails import enviar_email_recuperacion_password


#* RUTA PARA ACTIVAR USUARIO INICIAL
#22/06/25

class ActivarUsuarioInicialAPIView(generics.UpdateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioInicialActivarSerializer
    permission_classes = [AllowAny]
    lookup_field = 'username' #campo de filtro

    #metodo para ruta patch
    #22/06/25
    def patch(self, request, *args, **kwargs):
        usuario = self.get_object()
        serializer = self.get_serializer(usuario, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": "success",
                "message": "Usuario activado correctamente",
                "usuario": {
                    "username": usuario.get_username(),
                    "is_active": usuario.is_active
                }
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "message": "No se pudo activar el usuario",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

###############################################################################################

#* RUTA PARA VALIDAR CORREO PARA RECUPERAR CONTRASEÑA
#28/06/25

class ValidarUsernameRecuperarPasswordAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ValidarUsernameSerializer

    #método post para validar correo
    #28/06/25
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')

        #si el username llega vacío, envía este error
        if not username:
            return Response({
                "status": "error",
                "message": "Debe enviar el username."
            }, status=status.HTTP_400_BAD_REQUEST)

        #si el username no existe, envía este error
        try:
            usuario = Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            return Response({
                "status": "error",
                "message": "El usuario no existe."
            }, status=status.HTTP_404_NOT_FOUND)

        #envia email
        enviar_email_recuperacion_password(usuario)

        #respuesta OK
        return Response({
            "status": "success",
            "message": "Usuario existe, puede recuperar contraseña"
        }, status=status.HTTP_200_OK)

###############################################################################################

#* RUTA PARA RECUPERAR CONTRASEÑA
#28/06/25

class RecuperarPasswordAPIView(generics.UpdateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RecuperarPasswordSerializer
    permission_classes = [AllowAny]
    lookup_field = 'username'

    #método patch
    #28/06/25
    def patch(self, request, *args, **kwargs):
        usuario = self.get_object()
        serializer = self.get_serializer(usuario, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Contraseña actualizada correctamente",
                "usuario": usuario.get_username()
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "message": "No se pudo actualizar la contraseña",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)