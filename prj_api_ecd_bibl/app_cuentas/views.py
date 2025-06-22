from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, generics
from .serializers import UsuarioCreateAdminSerializer, UsuarioRegisterWebSerializer, UsuarioInicialActivarSerializer
from .models import Usuario
from django.db import IntegrityError
from rest_framework_simplejwt.views import TokenObtainPairView
from .jwt_serializers import CustomTokenObtainPairAdminSerializer, CustomTokenObtainPairWebSerializer
from .permissions import PermisoAdmin


#todo: generar mecanismo para enviar correo de activacion (ruta patch, etc...)
#todo: agregar header (cabecera) location

#RUTA DE VALIDACION DE SALUD DE LA API
#20/06/25

@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    return Response({"message": "API ECD Cuentas disponible"})

###############################################################################################
###############################################################################################

#* RUTAS POST

#RUTA PARA CREAR USUARIO (ADMIN)
#20/06/25

class CrearUsuarioAdminAPIView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioCreateAdminSerializer
    permission_classes = [PermisoAdmin] #permiso solo admin

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
                        "username": usuario.get_username(),
                        "rol": usuario.get_rol(),
                        "rol_nombre": usuario.get_rol_display()
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
###############################################################################################

#* LOGIN Y LOGOUT

#LOGIN ADMIN CON JWT
#21/06/25

class CustomTokenObtainPairAdminView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairAdminSerializer

###############################################################################################

#LOGIN WEB CON JWT
#21/06/25

class CustomTokenObtainPairWebView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairWebSerializer

#todo: falta el logout

###############################################################################################
###############################################################################################

#* RUTAS GET

###############################################################################################
###############################################################################################

#* RUTAS PUT

###############################################################################################
###############################################################################################

#* RUTAS PATCH

#RUTA PARA ACTIVAR USUARIO INICIAL
#22/06/25

class ActivarUsuarioInicialAPIView(generics.UpdateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioInicialActivarSerializer
    permission_classes = [AllowAny]

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
###############################################################################################

#* RUTAS DELETE