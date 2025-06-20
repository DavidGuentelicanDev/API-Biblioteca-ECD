"""
Aquí irán todos los serializers para crear rutas de app_cuentas
"""

from rest_framework import serializers
from .models import Usuario


#* SERIALIZERS POST

#CREAR USUARIO
#20/06/25

class UsuarioCreateAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

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

    def create(self, validated_data):
        password = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario

#todo: validar respuesta al crear, solo status, mensaje y error
#todo: validar que solo pueda ser rol 1 a 3
#todo: validar formato rut y telefono