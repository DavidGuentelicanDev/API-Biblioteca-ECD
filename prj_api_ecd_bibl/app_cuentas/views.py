from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, generics
from .serializers.general import UsuarioInicialActivarSerializer, UsuarioActualizarPasswordSerializer
from .serializers.jwt import CustomTokenObtainPairAdminSerializer, CustomTokenObtainPairWebSerializer
from .serializers.admin import UsuarioCreateAdminSerializer, UsuarioAdminListSerializer, UsuarioAdminUpdateSerializer
from .serializers.web import UsuarioRegisterWebSerializer, UsuarioWebListSerializer, UsuarioWebUpdateSerializer
from .models import Usuario
from django.db import IntegrityError
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import PermisoAdmin, PermisoCliente, PermisoFuncionario
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView


#todo: reorganizar el codigo en archivos modulares

#RUTA DE VALIDACION DE SALUD DE LA API
#20/06/25

@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    return Response({"message": "API Biblioteca ECD Cuentas disponible"})

###############################################################################################
###############################################################################################

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

#* RUTAS POST

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

###############################################################################################

#LOGOUT CON JWT
#22/06/25

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                "status": "success",
                "message": "Sesión cerrada correctamente. Refresh token inhabilitado correctamente."
            }, status=status.HTTP_200_OK) #HTTP_205_RESET_CONTENT para usar respuesta correcta
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Token inválido o ya fue deshabilitado."
            }, status=status.HTTP_400_BAD_REQUEST)

###############################################################################################
###############################################################################################

#* RUTAS GET

###############################################################################################

#RUTA PARA OBTENER USUARIO POR ID (ADMIN)
#22/06/25

class UsuarioAdminRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioAdminListSerializer
    permission_classes = [PermisoFuncionario]

###############################################################################################

#RUTA PARA OBTENER USUARIO POR ID (WEB)
#24/06/25

class UsuarioWebRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioWebListSerializer
    permission_classes = [PermisoCliente]

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