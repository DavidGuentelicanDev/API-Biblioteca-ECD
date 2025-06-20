from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import UsuarioCreateAdminSerializer
from rest_framework.views import APIView
from rest_framework import generics
from .models import Usuario
from django.db import IntegrityError


#* RUTA DE VALIDACION DE SALUD DE LA API
#20/06/25

@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    return Response({"message": "API ECD Cuentas disponible"})

###############################################################################################

#* RUTAS POST

#RUTA PARA REGISTRAR USUARIO
#20/06/25

class CrearUsuarioAdminAPIView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioCreateAdminSerializer
    permission_classes = [AllowAny]

    #metodo create personalizado
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                self.perform_create(serializer)
            except IntegrityError as e:
                return Response(
                    {
                        "status": "error",
                        "message": "Hubo un error al crear el usuario",
                        "errors": {"telefono": ["El teléfono ya existe o es inválido."]}
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            headers = self.get_success_headers(serializer.data)
            return Response(
                {
                    "status": "success",
                    "message": "Usuario creado correctamente",
                    "usuario": serializer.data
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

#todo: quitarle allowany luego de crear ruta de login
#todo: restringir permisos a cierto tipo de usuario