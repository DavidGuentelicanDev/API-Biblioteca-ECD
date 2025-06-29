"""
STATUS DE API CUENTAS
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


#* RUTA DE VALIDACION DE SALUD DE LA API
#20/06/25

@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    return Response({"message": "API Biblioteca ECD Cuentas disponible"})