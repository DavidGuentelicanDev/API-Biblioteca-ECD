"""
SERIALIZERS PARA EL SISTEMA JWT
"""

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


#GENERA LOS TOKEN JWT PARA AUTENTICACIÓN ADMIN
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


#GENERA LOS TOKEN JWT PARA AUTENTICACIÓN WEB
#21/06/25

class CustomTokenObtainPairWebSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        usuario = self.user

        #solo permite usuarios cliente y admin (rol 4 y 1)
        if not usuario.rol in [1, 4]:
            raise serializers.ValidationError("Los usuarios rol 2 y 3 no pueden loguearse en la página web.")

        data['usuario'] = {
            "username": usuario.get_username(),
            "rol": usuario.get_rol(),
            "rol_nombre": usuario.get_rol_display(),
            "nombre_completo": usuario.get_full_name()
        }
        return data