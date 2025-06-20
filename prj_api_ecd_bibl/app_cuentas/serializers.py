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
        return value

    #metodo para validar rol
    #20/06/25
    def validate_rol(self, value):
        #solo se permiten valores de 1 a 3 (rol 4 queda excluido en esta ruta)
        if value not in [1, 2, 3]:
            raise serializers.ValidationError("Solo se permite crear usuarios con rol Administrador, Bibliotecario o Funcionario.")
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

#todo: validar que solo pueda ser rol 1 a 3, y siempre is_staff=True
#todo: validar formato rut y telefono