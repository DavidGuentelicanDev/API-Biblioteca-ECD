"""
SERIALIZERS PARA EL SISTEMA JWT
"""

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


#GENERA LOS TOKEN JWT PARA AUTENTICACIÓN
#21/06/25

class CustomTokenObtainPairAdminSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        usuario = self.user

        #solo permite usuarios staff (rol 1 - 3)
        if not usuario.is_staff:
            raise serializers.ValidationError("No tiene permisos para acceder a este sistema.")

        data['usuario'] = {
            "username": usuario.get_username(),
            "rol": usuario.get_rol(),
            "rol_nombre": usuario.get_rol_display(),
            "nombre_completo": usuario.get_full_name()
        }
        return data