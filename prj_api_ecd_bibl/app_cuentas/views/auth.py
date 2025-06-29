"""
RUTAS DE AUTENTIFICACIÓN DE LA API CUENTAS
"""

from rest_framework_simplejwt.views import TokenObtainPairView
from ..serializers.jwt import CustomTokenObtainPairAdminSerializer, CustomTokenObtainPairWebSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status


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
            }, status=status.HTTP_205_RESET_CONTENT) #HTTP_205_RESET_CONTENT para usar respuesta correcta
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Token inválido o ya fue deshabilitado."
            }, status=status.HTTP_400_BAD_REQUEST)