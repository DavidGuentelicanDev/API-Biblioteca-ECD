"""
SERIALIZERS DE RUTAS DE USUARIO (GET, POST)
"""

from rest_framework import serializers
from .models import Usuario
import re
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model


#* SERIALIZERS POST

#CREAR USUARIO
#20/06/25

class UsuarioCreateAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    #estructura json a enviar en el body
    class Meta:
        model = Usuario
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'rut',
            'telefono',
            'rol',
            'foto_perfil'
        ]

    #metodo para validaciones de telefono
    #20/06/25
    def validate_telefono(self, value):
        #si el valor de telefono es "", lo convierte en None (null)
        if value == "":
            return None
        #formato telefono +569XXXXXXXX
        patron = r'^\+569\d{8}$'
        if not re.match(patron, value):
            raise serializers.ValidationError(
                "El teléfono debe tener formato +569XXXXXXXX, donde X son números"
            )
        return value

    #metodo para validar rol
    #20/06/25
    def validate_rol(self, value):
        #solo se permiten valores de 1 a 3 (rol 4 queda excluido en esta ruta)
        if value not in [1, 2, 3]:
            raise serializers.ValidationError("Solo se permite crear usuarios con rol Administrador, Bibliotecario o Funcionario.")
        return value

    #metodo para validar formato de rut
    #20/06/25
    def validate_rut(self, value):
        #formato rut XXXXXXXX-K
        patron = r'^\d{7,8}-[\dkK]$'
        if not re.match(patron, value):
            raise serializers.ValidationError(
                "El RUT debe tener el formato XXXXXXXX-K, donde X son números y K es un número o la letra k/K."
            )
        return value

    #metodo para validar condiciones necesarias de la password
    #usa las validaciones nativas de django
    #20/06/25
    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    #metodo create para el guardado personalizado
    #20/06/25
    def create(self, validated_data):
        password = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.is_staff = True #siempre staff
        usuario.set_password(password)
        usuario.save()
        return usuario

########################################################################################