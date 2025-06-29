"""
SERIALIZERS DE RUTAS DE USUARIO GENERALES
"""

from rest_framework import serializers
from ..models import Usuario
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError


#ACTIVAR USUARIO INICIAL
#22/06/25

class UsuarioInicialActivarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['is_active']
        read_only_fields = []

################################################################################################

#* SERIALIZER PARA VALIDAR USERNAME PARA RECUPERACIÓN DE CONTRASEÑA
#28/06/25

class ValidarUsernameSerializer(serializers.Serializer):
    username = serializers.CharField()

###############################################################################################

#* SERIALIZER PARA RECUPERAR CONTRASEÑA
#28/06/25

class RecuperarPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    #método para validar contraseña con lo incorporado con django
    #28/06/25
    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    #método update
    #28/06/25
    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance