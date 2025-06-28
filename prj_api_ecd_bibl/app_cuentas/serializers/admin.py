"""
SERIALIZERS DE RUTAS DE USUARIO ADMIN
"""

from rest_framework import serializers
from ..models import Usuario
from ..utils.validations import validate_telefono, validate_rut
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from ..utils.emails import enviar_email_bienvenida_usuario_nuevo_staff


#CREAR USUARIO (ADMIN)
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
            'rol'
        ]

    #metodo para validaciones de telefono
    #20/06/25
    def validate_telefono(self, value):
        return validate_telefono(value)

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
        return validate_rut(value)

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
        usuario.is_staff = True #siempre creado staff
        usuario.is_active = False #siempre creado inactivo
        usuario.set_password(password)
        usuario.save()

        #enviar correo al crear
        enviar_email_bienvenida_usuario_nuevo_staff(usuario)

        return usuario

################################################################################################

#OBTENER TODOS LOS USUARIOS ADMIN
#22/06/25

class UsuarioAdminListSerializer(serializers.ModelSerializer):
    rol = serializers.SerializerMethodField()
    foto_perfil_url = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'rut',
            'telefono',
            'rol',
            'is_active',
            'date_joined',
            'last_login',
            'foto_perfil_url'
        ]

    #método para obtener el rol como objeto
    #28/06/25
    def get_rol(self, obj):
        return {
            "numero": obj.rol,
            "nombre": obj.get_rol_display()
        }

    #método para obtener la url de la foto de perfil
    #22/06/25
    def get_foto_perfil_url(self, obj):
        return obj.get_foto_perfil()

################################################################################################

#ACTUALIZAR DATOS DE USUARIO ADMIN (MENOS DATOS SENSIBLES)
#23/06/25

class UsuarioAdminUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        #campos excluídos
        exclude = [
            'password',
            'last_login',
            'is_staff',
            'is_superuser',
            'date_joined',
            'groups',
            'user_permissions',
            'foto_perfil',
            'username'
        ]

    #metodo para validaciones de telefono
    #23/06/25
    def validate_telefono(self, value):
        return validate_telefono(value)

    #metodo para validar rol
    #23/06/25
    def validate_rol(self, value):
        #solo se permiten valores de 1 a 3 (rol 4 queda excluido en esta ruta)
        if value not in [1, 2, 3]:
            raise serializers.ValidationError("Solo se permite editar rol Administrador, Bibliotecario o Funcionario.")
        return value

    #metodo para validar formato de rut
    #23/06/25
    def validate_rut(self, value):
        return validate_rut(value)