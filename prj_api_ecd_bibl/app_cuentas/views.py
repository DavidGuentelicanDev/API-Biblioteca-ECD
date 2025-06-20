from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import UsuarioCreateAdminSerializer
from rest_framework.views import APIView
from rest_framework import generics
from .models import Usuario


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