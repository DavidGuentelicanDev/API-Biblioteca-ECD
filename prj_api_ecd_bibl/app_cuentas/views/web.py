"""
RUTAS DE WEB DE LA API CUENTAS
"""

from rest_framework import generics
from ..models import Usuario
from ..serializers.web import UsuarioRegisterWebSerializer, UsuarioWebListSerializer, UsuarioWebUpdateSerializer
from rest_framework.permissions import AllowAny
from ..utils.permissions import PermisoCliente


#RUTA PARA REGISTRAR USUARIO (WEB)
#21/06/25

class RegistrarUsuarioWebAPIView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioRegisterWebSerializer
    permission_classes = [AllowAny]

    #metodo create personalizado
    #20/06/25
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) #obtiene los datos del json

        if serializer.is_valid():
            #si es valido, intenta crear
            try:
                self.perform_create(serializer)
            except IntegrityError as e:
                #respuesta json en caso de que el telefono sea invalido
                return Response(
                    {
                        "status": "error",
                        "message": "Hubo un error al crear el usuario",
                        "errors": {"telefono": ["El teléfono ya existe o es inválido."]}
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            usuario = serializer.instance #el usuario recien creado
            headers = self.get_success_headers(serializer.data) #obtiene los datos serializados para la respuesta json
            return Response(
                {
                    "status": "success",
                    "message": f"Usuario {usuario.get_username()} creado correctamente",
                    "usuario": {
                        "id": usuario.pk,
                        "username": usuario.get_username()
                    }
                },
                status=status.HTTP_201_CREATED,
                headers=headers
            )

        return Response(
            {
                "status": "error",
                "message": "Hubo un error al crear el usuario",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

###############################################################################################

#RUTA PARA OBTENER USUARIO POR ID (WEB)
#24/06/25

class UsuarioWebRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioWebListSerializer
    permission_classes = [PermisoCliente]

###############################################################################################

#RUTA PARA ACTUALIZAR DATOS DE USUARIO (WEB)
#24/06/25

class UsuarioWebUpdateAPIView(generics.UpdateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioWebUpdateSerializer
    permission_classes = [PermisoCliente]

    #metodo patch
    #24/06/25
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