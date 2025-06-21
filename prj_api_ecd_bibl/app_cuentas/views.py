from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import UsuarioCreateAdminSerializer, LoginAdminSerializer
from rest_framework import generics
from .models import Usuario
from django.db import IntegrityError
from rest_framework.views import APIView


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

#todo: quitarle allowany luego de crear ruta de login
#todo: restringir permisos a cierto tipo de usuario
#todo: usuario siempre se crea is_active=False
#todo: generar mecanismo para enviar correo de activacion (ruta patch, etc...)
#todo: agregar header (cabecera) location

class CrearUsuarioAdminAPIView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioCreateAdminSerializer
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
                    "usuario": usuario.get_username()
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

#RUTA DE LOGIN ADMIN
#20/06/25

class LoginAdminAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginAdminSerializer

    #funcion para enviar datos post para login
    #20/06/25
    def post(self, request):
        serializer = LoginAdminSerializer(data=request.data)

        if serializer.is_valid():
            usuario = serializer.validated_data['usuario']

            return Response({
                "status": "success",
                "message": "Login exitoso",
                "usuario": {
                    "username": usuario.get_username(),
                    "rol": usuario.get_rol(),
                    "nombre_completo": usuario.get_full_name()
                }
            }, status=status.HTTP_200_OK,)

        return Response({
            "status": "error",
            "message": "Hubo un error al iniciar sesión",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)