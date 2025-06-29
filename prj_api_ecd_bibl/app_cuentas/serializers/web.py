"""
SERIALIZERS DE RUTAS DE USUARIO WEB
"""

from rest_framework import serializers
from ..models import Usuario
from django.core.validators import validate_email
from ..utils.validations import validate_telefono, validate_rut
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from ..utils.emails import enviar_email_bienvenida_usuario_nuevo_cliente


#* REGISTRAR USUARIO (WEB)
#21/06/25

class UsuarioRegisterWebSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        #estructura json a enviar en el body
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

    #metodo para validar formato uusername (correo)
    #21/06/25
    def validate_username(self, value):
        try:
            validate_email(value)
        except serializers.ValidationError:
            raise serializers.ValidationError("El nombre de usuario debe ser un correo electrónico válido.")
        return value

    #validacion para que username e email sean iguales
    #21/06/25
    def validate(self, data):
        if data.get('username') != data.get('email'):
            raise serializers.ValidationError("El nombre de usuario y el correo electrónico deben ser iguales.")
        return data

    #metodo para validaciones de telefono
    #20/06/25
    def validate_telefono(self, value):
        return validate_telefono(value)

    #metodo para validar rol
    #21/06/25
    def validate_rol(self, value):
        #solo se permite valor 4 (clientes)
        if value != 4:
            raise serializers.ValidationError("Solo se permite crear usuarios con rol Cliente.")
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
        usuario.is_staff = False #nunca creado staff
        usuario.is_active = False #siempre creado inactivo
        usuario.set_password(password)
        usuario.save()

        #enviar correo al crear
        enviar_email_bienvenida_usuario_nuevo_cliente(usuario)

        return usuario

################################################################################################

#* OBTENER TODOS LOS USUARIOS WEB
#24/06/25

class UsuarioWebRetrieveSerializer(serializers.ModelSerializer):
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
            'date_joined',
            'foto_perfil_url'
        ]

    #método para obtener la url de la foto de perfil
    #24/06/25
    def get_foto_perfil_url(self, obj):
        return obj.get_foto_perfil()

################################################################################################

#* ACTUALIZAR DATOS DE USUARIO WEB (MENOS DATOS SENSIBLES)
#24/06/25

class UsuarioWebUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        #campos excluídos
        exclude = [
            'last_login',
            'is_staff',
            'is_superuser',
            'date_joined',
            'groups',
            'user_permissions',
            'rol',
            'is_active'
        ]
        #campos que si se modifican
        #first_name, last_name, rut, telefono, username, email, password

    #metodo para validar formato uusername (correo)
    #24/06/25
    def validate_username(self, value):
        try:
            validate_email(value)
        except serializers.ValidationError:
            raise serializers.ValidationError("El nombre de usuario debe ser un correo electrónico válido.")
        return value

    #validacion para que username e email sean iguales
    #24/06/25
    def validate(self, data):
        if data.get('username') != data.get('email'):
            raise serializers.ValidationError("El nombre de usuario y el correo electrónico deben ser iguales.")
        return data

    #metodo para validaciones de telefono
    #23/06/25
    def validate_telefono(self, value):
        return validate_telefono(value)

    #metodo para validar formato de rut
    #23/06/25
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