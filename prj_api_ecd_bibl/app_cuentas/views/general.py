"""
RUTAS GENERALES DE LA API CUENTAS
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from ..models import Usuario
from ..serializers.general import UsuarioInicialActivarSerializer, UsuarioActualizarPasswordSerializer


#RUTA DE VALIDACION DE SALUD DE LA API
#20/06/25

@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    return Response({"message": "API Biblioteca ECD Cuentas disponible"})

###############################################################################################

#RUTA PARA ACTIVAR USUARIO INICIAL
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
                    "id": usuario.pk,
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

#RUTA PARA ACTUALIZAR CONTRASEÑA
#24/06/25

class UsuarioActualizarPasswordAPIView(generics.UpdateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioActualizarPasswordSerializer
    permission_classes = [IsAuthenticated]

    #metodo patch
    #24/06/25
    def patch(self, request, *args, **kwargs):
        usuario = self.get_object()
        serializer = self.get_serializer(usuario, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Contraseña actualizada correctamente",
                "usuario": {
                    "id": usuario.pk,
                    "username": usuario.get_username()
                }
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "message": "No se pudo actualizar la contraseña",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)