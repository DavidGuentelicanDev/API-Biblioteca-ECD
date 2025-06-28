"""
RUTAS DE WEB DE LA API CUENTAS
"""

from rest_framework import generics, status
from ..models import Usuario
from ..serializers.web import (
    UsuarioRegisterWebSerializer,
    UsuarioWebRetrieveSerializer,
    UsuarioWebUpdateSerializer
)
from rest_framework.permissions import AllowAny
from ..utils.permissions import PermisoCliente
from rest_framework.response import Response
from rest_framework.exceptions import NotFound


#* RUTA PARA REGISTRAR USUARIO (WEB)
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
                    "message": f"Usuario {usuario.get_username()} creado correctamente."
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

#* RUTA PARA OBTENER DATOS DE USUARIO CLIENTE | ACTUALIZAR DATOS
#28/06/25

class UsuarioWebRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Usuario.objects.all()
    permission_classes = [PermisoCliente]
    lookup_field = 'username'

    #método get object para limitar filtro a rol = 4 (cliente)
    #28/06/25
    def get_object(self):
        obj = super().get_object()
        if obj.rol != 4:
            raise NotFound("No existe un usuario cliente con ese username.")
        return obj

    #método para definir serializer segun método HTTP
    #28/06/25
    def get_serializer_class(self):
        #si es GET, serializer UsuarioWebRetrieveSerializer
        if self.request.method == 'GET':
            return UsuarioWebRetrieveSerializer
        #si es PUT/PATCH, serializer UsuarioWebUpdateSerializer
        return UsuarioWebUpdateSerializer

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