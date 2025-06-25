"""
SERIALIZERS DE RUTAS DE USUARIO GENERALES
"""

from rest_framework import serializers
from ..models import Usuario
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError


#todo pendiente: ruta para recuperar contraseña aparte integrando validaciones de django

#ACTIVAR USUARIO INICIAL
#22/06/25

class UsuarioInicialActivarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['is_active']
        read_only_fields = []

################################################################################################

#ACTUALIZAR CONTRASEÑA
#24/06/25

class UsuarioActualizarPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    #validadores de contraseña de django
    #24/06/25
    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    #guardar contraseña nueva
    #24/06/25
    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance